#!/usr/bin/env Rscript

# Repair SPY_daily_measures.csv from local 5-minute bar files.
#
# scripts/download_spy_taq_wrds.R writes an all-NA row (with an `error` column)
# for any trading day on which the WRDS query failed, e.g. after a network
# drop. When the corresponding bar file
#   data/taq_spy/bars_5min/SPY_YYYYMMDD_5min.csv.gz
# exists from an earlier successful run, the daily measures can be recomputed
# locally without touching WRDS. This script does exactly that, using the same
# formulas as download_one_day() in the download script:
#   rv    = sum of squared 5-minute log returns (x100, i.e. squared percent)
#   rskew = highfrequency::rSkew(returns)
#   rkurt = highfrequency::rKurt(returns)
# n_intraday (number of cleaned trades) is not recoverable from the bars and is
# left NA on repaired rows.
#
# Requirements:
#   install.packages(c("data.table", "highfrequency"))

usage <- function() {
  cat(
    "Usage:\n",
    "  Rscript scripts/repair_spy_daily_measures_from_bars.R [options]\n\n",
    "Options:\n",
    "  --csv FILE       Daily measures CSV. Default: data/taq_spy/SPY_daily_measures.csv\n",
    "  --bars-dir DIR   Directory with 5-minute bar files. Default: data/taq_spy/bars_5min\n",
    "  --symbol SYMBOL  Symbol prefix in filenames. Default: SPY\n",
    "  --check-only     Recompute every row that has a bar file and report the maximum\n",
    "                   discrepancy against the CSV, without writing anything.\n",
    "  --help           Show this message\n",
    sep = ""
  )
}

parse_args <- function(args) {
  defaults <- list(
    csv = "data/taq_spy/SPY_daily_measures.csv",
    bars_dir = "data/taq_spy/bars_5min",
    symbol = "SPY",
    check_only = "false"
  )
  if (any(args %in% c("--help", "-h"))) {
    usage()
    quit(status = 0)
  }
  i <- 1
  while (i <= length(args)) {
    arg <- args[[i]]
    if (!startsWith(arg, "--")) stop("Unexpected positional argument: ", arg, call. = FALSE)
    if (grepl("=", arg, fixed = TRUE)) {
      parts <- strsplit(sub("^--", "", arg), "=", fixed = TRUE)[[1]]
      key <- parts[[1]]
      value <- paste(parts[-1], collapse = "=")
    } else {
      key <- sub("^--", "", arg)
      if (i == length(args) || startsWith(args[[i + 1]], "--")) {
        value <- "true"
      } else {
        i <- i + 1
        value <- args[[i]]
      }
    }
    key <- gsub("-", "_", key)
    if (!key %in% names(defaults)) stop("Unknown option: --", gsub("_", "-", key), call. = FALSE)
    defaults[[key]] <- value
    i <- i + 1
  }
  defaults
}

suppressPackageStartupMessages({
  library(data.table)
  library(highfrequency)
})

args <- parse_args(commandArgs(trailingOnly = TRUE))
csv_path <- args$csv
bars_dir <- args$bars_dir
symbol <- toupper(args$symbol)
check_only <- tolower(args$check_only) %in% c("true", "t", "1", "yes", "y")

if (!file.exists(csv_path)) stop("CSV not found: ", csv_path, call. = FALSE)
if (!dir.exists(bars_dir)) stop("Bars directory not found: ", bars_dir, call. = FALSE)

daily <- fread(csv_path)
daily[, date := as.Date(date)]
if (!"error" %in% names(daily)) daily[, error := NA_character_]

# Same computation as download_one_day() in scripts/download_spy_taq_wrds.R.
measures_from_bars <- function(bars_path, date_value) {
  bars <- fread(bars_path)
  setorder(bars, DT)
  bars[, ret := 100 * (log(PRICE) - shift(log(PRICE), type = "lag"))]
  returns <- bars[!is.na(ret), ret]
  data.table(
    date = date_value,
    symbol = symbol,
    n_intraday = NA_integer_,
    n_bars = nrow(bars),
    open_taq = bars$PRICE[1],
    close_taq = bars$PRICE[nrow(bars)],
    rv = sum(returns^2),
    rskew = if (length(returns) > 0) highfrequency::rSkew(returns) else NA_real_,
    rkurt = if (length(returns) > 0) highfrequency::rKurt(returns) else NA_real_,
    error = NA_character_
  )
}

bars_path_for <- function(d) {
  file.path(bars_dir, sprintf("%s_%s_5min.csv.gz", symbol, format(d, "%Y%m%d")))
}

if (check_only) {
  have_bars <- daily[file.exists(bars_path_for(date)) & !is.na(rv)]
  message("Recomputing ", nrow(have_bars), " rows that have both a bar file and a stored rv.")
  recomputed <- rbindlist(lapply(seq_len(nrow(have_bars)), function(i) {
    measures_from_bars(bars_path_for(have_bars$date[i]), have_bars$date[i])
  }))
  cmp <- merge(have_bars[, .(date, rv, rskew, rkurt, n_bars)],
               recomputed[, .(date, rv2 = rv, rskew2 = rskew, rkurt2 = rkurt, n_bars2 = n_bars)],
               by = "date")
  cat(sprintf("max |rv - rv2|     = %.3e\n", max(abs(cmp$rv - cmp$rv2))))
  cat(sprintf("max |rskew - rskew2| = %.3e\n", max(abs(cmp$rskew - cmp$rskew2), na.rm = TRUE)))
  cat(sprintf("max |rkurt - rkurt2| = %.3e\n", max(abs(cmp$rkurt - cmp$rkurt2), na.rm = TRUE)))
  cat(sprintf("n_bars mismatches    = %d\n", sum(cmp$n_bars != cmp$n_bars2)))
  quit(status = 0)
}

to_repair <- daily[is.na(rv) & file.exists(bars_path_for(date)), date]
message("Rows with missing rv and an existing bar file: ", length(to_repair))
if (length(to_repair) == 0) {
  message("Nothing to repair.")
  quit(status = 0)
}

repaired <- rbindlist(lapply(to_repair, function(d) measures_from_bars(bars_path_for(d), d)))
if (any(is.na(repaired$rv))) {
  stop("Recomputation produced NA rv for: ",
       paste(format(repaired[is.na(rv), date]), collapse = ", "), call. = FALSE)
}

# Replace the failed rows in place; keep column order and every other row untouched.
daily <- daily[!date %in% to_repair]
daily <- rbindlist(list(daily, repaired), use.names = TRUE, fill = TRUE)
setorder(daily, date)
setcolorder(daily, intersect(c("date", "symbol", "n_intraday", "n_bars", "open_taq",
                               "close_taq", "rv", "rskew", "rkurt", "error"), names(daily)))

backup <- sprintf("%s.bak-%s", csv_path, format(Sys.Date(), "%Y%m%d"))
if (!file.exists(backup)) file.copy(csv_path, backup)
fwrite(daily, csv_path)

message("Repaired ", nrow(repaired), " rows: ",
        format(min(repaired$date)), " to ", format(max(repaired$date)), ".")
message("Backup of the previous CSV: ", backup)
message("Remaining rows without rv: ", sum(is.na(daily$rv)),
        " (", format(min(daily[is.na(rv), date])), " onward)")
