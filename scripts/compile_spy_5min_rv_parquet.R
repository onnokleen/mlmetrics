#!/usr/bin/env Rscript

# Compile daily realized measures from local SPY 5-minute TAQ bar files.
#
# Input files are expected to be produced by scripts/download_spy_taq_wrds.R:
#   data/taq_spy/bars_5min/SPY_YYYYMMDD_5min.csv.gz
#
# Output is private/local by default because data/taq_spy/ is gitignored.

usage <- function() {
  cat(
    "Usage:\n",
    "  Rscript scripts/compile_spy_5min_rv_parquet.R [options]\n\n",
    "Options:\n",
    "  --bars-dir DIR        Directory with 5-minute bar CSV files. Default: data/taq_spy/bars_5min\n",
    "  --out FILE            Output Parquet file. Default: data/taq_spy/SPY_5min_daily_rv.parquet\n",
    "  --symbol SYMBOL       Symbol prefix in input filenames. Default: SPY\n",
    "  --help                Show this message\n\n",
    "Example:\n",
    "  Rscript scripts/compile_spy_5min_rv_parquet.R\n",
    sep = ""
  )
}

parse_args <- function(args) {
  defaults <- list(
    bars_dir = "data/taq_spy/bars_5min",
    out = "data/taq_spy/SPY_5min_daily_rv.parquet",
    symbol = "SPY"
  )

  if (any(args %in% c("--help", "-h"))) {
    usage()
    quit(status = 0)
  }

  i <- 1
  while (i <= length(args)) {
    arg <- args[[i]]
    if (!startsWith(arg, "--")) {
      stop("Unexpected positional argument: ", arg, call. = FALSE)
    }

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
    if (!key %in% names(defaults)) {
      stop("Unknown option: --", gsub("_", "-", key), call. = FALSE)
    }
    defaults[[key]] <- value
    i <- i + 1
  }

  defaults
}

suppressPackageStartupMessages({
  library(data.table)
  library(arrow)
})

args <- parse_args(commandArgs(trailingOnly = TRUE))
bars_dir <- args$bars_dir
out_file <- args$out
symbol <- toupper(args$symbol)

if (!dir.exists(bars_dir)) {
  stop("Bars directory does not exist: ", bars_dir, call. = FALSE)
}

pattern <- sprintf("^%s_[0-9]{8}_5min\\.csv\\.gz$", symbol)
bar_files <- list.files(bars_dir, pattern = pattern, full.names = TRUE)
bar_files <- sort(bar_files)

if (length(bar_files) == 0) {
  stop("No matching 5-minute bar files found in: ", bars_dir, call. = FALSE)
}

message("Found ", length(bar_files), " bar files.")

measure_one_file <- function(path) {
  file_name <- basename(path)
  date_key <- sub(sprintf("^%s_([0-9]{8})_5min\\.csv\\.gz$", symbol), "\\1", file_name)
  date_value <- as.Date(date_key, format = "%Y%m%d")

  bars <- fread(path)
  required_cols <- c("DT", "PRICE")
  missing_cols <- setdiff(required_cols, names(bars))
  if (length(missing_cols) > 0) {
    stop("Missing required columns in ", path, ": ", paste(missing_cols, collapse = ", "), call. = FALSE)
  }

  setorder(bars, DT)
  bars <- bars[!is.na(PRICE) & PRICE > 0]
  if (nrow(bars) < 2) {
    return(data.table(
      date = date_value,
      symbol = symbol,
      n_bars = nrow(bars),
      open_taq = if (nrow(bars) == 1) bars$PRICE[1] else NA_real_,
      close_taq = if (nrow(bars) == 1) bars$PRICE[1] else NA_real_,
      rv_5min = NA_real_,
      bv_5min = NA_real_,
      rq_5min = NA_real_,
      intraday_return = NA_real_
    ))
  }

  log_price <- log(bars$PRICE)
  ret <- diff(log_price)
  ret_pct <- 100 * ret

  data.table(
    date = date_value,
    symbol = symbol,
    n_bars = nrow(bars),
    open_taq = bars$PRICE[1],
    close_taq = bars$PRICE[nrow(bars)],
    rv_5min = sum(ret_pct^2),
    bv_5min = (pi / 2) * sum(abs(ret_pct[-1]) * abs(ret_pct[-length(ret_pct)])),
    rq_5min = (length(ret_pct) / 3) * sum(ret_pct^4),
    intraday_return = 100 * (log_price[length(log_price)] - log_price[1])
  )
}

daily <- rbindlist(lapply(bar_files, measure_one_file), use.names = TRUE, fill = TRUE)
setorder(daily, date)

dir.create(dirname(out_file), recursive = TRUE, showWarnings = FALSE)
arrow::write_parquet(daily, out_file)

message("Wrote ", nrow(daily), " daily rows to: ", normalizePath(out_file, mustWork = FALSE))
