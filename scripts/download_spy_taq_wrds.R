#!/usr/bin/env Rscript

# Download and clean SPY TAQ millisecond trades from WRDS.
#
# This follows the workflow described at:
# https://onnokleen.com/post/taq_via_wrds/
#
# Requirements:
#   install.packages(c("DBI", "RPostgres", "data.table", "lubridate", "highfrequency"))
#
# Authentication:
#   Prefer a ~/.pgpass entry for wrds-pgdata.wharton.upenn.edu:9737:wrds:<user>:<password>.
#   Alternatively set WRDS_USER and WRDS_PASSWORD in the environment.

usage <- function() {
  cat(
    "Usage:\n",
    "  Rscript scripts/download_spy_taq_wrds.R [options]\n\n",
    "Options:\n",
    "  --symbol SYMBOL              TAQ root symbol. Default: SPY\n",
    "  --start YYYY-MM-DD           Start date. Default: 2015-01-01\n",
    "  --end YYYY-MM-DD             End date. Default: 2025-12-31\n",
    "  --out DIR                    Output directory. Default: data/taq_spy\n",
    "  --user USER                  WRDS username. Default: WRDS_USER env var\n",
    "  --exchanges LIST             Comma-separated TAQ exchange codes. Default: N,T,Q,A,P\n",
    "  --aggregate-minutes N        Intraday bar length in minutes. Default: 5\n",
    "  --save-clean-trades BOOL     Save cleaned trade files. Default: false\n",
    "  --overwrite BOOL             Re-download existing daily outputs. Default: false\n",
    "  --max-days N                 Optional cap for testing. Default: all available days\n",
    "  --dry-run BOOL               List available dates but do not download. Default: false\n",
    "  --help                       Show this message\n\n",
    "Examples:\n",
    "  WRDS_USER=my_wrds_id Rscript scripts/download_spy_taq_wrds.R\n",
    "  Rscript scripts/download_spy_taq_wrds.R --start 2015-01-01 --end 2015-01-31 --max-days 3\n",
    "  Rscript scripts/download_spy_taq_wrds.R --save-clean-trades true\n",
    sep = ""
  )
}

parse_args <- function(args) {
  defaults <- list(
    symbol = "SPY",
    start = "2020-04-01",
    end = "2024-12-31",
    out = "data/taq_spy",
    user = Sys.getenv("WRDS_USER", unset = ""),
    exchanges = "N,T,Q,A,P",
    aggregate_minutes = "5",
    save_clean_trades = "false",
    overwrite = "false",
    max_days = "",
    dry_run = "false"
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

as_bool <- function(x) {
  value <- tolower(trimws(as.character(x)))
  if (value %in% c("true", "t", "1", "yes", "y")) return(TRUE)
  if (value %in% c("false", "f", "0", "no", "n")) return(FALSE)
  stop("Expected a boolean value, got: ", x, call. = FALSE)
}

args <- parse_args(commandArgs(trailingOnly = TRUE))

suppressPackageStartupMessages({
  library(DBI)
  library(RPostgres)
  library(data.table)
  library(lubridate)
  library(highfrequency)
})

if (interactive() && length(commandArgs(trailingOnly = TRUE)) == 0) {
  stop(
    paste(
      "This is a command-line download script and should be run with Rscript, not source().",
      "From RStudio, use:",
      "system2('Rscript', c('scripts/download_spy_taq_wrds.R', '--start', '2015-01-01', '--end', '2015-01-31', '--max-days', '1'))",
      sep = "\n"
    ),
    call. = FALSE
  )
}

symbol <- toupper(args$symbol)
start_date <- as.Date(args$start)
end_date <- as.Date(args$end)
out_dir <- args$out
wrds_user <- args$user
exchanges <- trimws(strsplit(args$exchanges, ",", fixed = TRUE)[[1]])
aggregate_minutes <- as.integer(args$aggregate_minutes)
save_clean_trades <- as_bool(args$save_clean_trades)
overwrite <- as_bool(args$overwrite)
dry_run <- as_bool(args$dry_run)
max_days <- if (nzchar(args$max_days)) as.integer(args$max_days) else NA_integer_

if (is.na(start_date) || is.na(end_date) || start_date > end_date) {
  stop("Invalid date range.", call. = FALSE)
}
if (!nzchar(wrds_user)) {
  stop("Provide a WRDS username via --user or WRDS_USER.", call. = FALSE)
}
if (is.na(aggregate_minutes) || aggregate_minutes <= 0) {
  stop("--aggregate-minutes must be a positive integer.", call. = FALSE)
}

bars_dir <- file.path(out_dir, sprintf("bars_%dmin", aggregate_minutes))
trades_dir <- file.path(out_dir, "clean_trades")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(bars_dir, recursive = TRUE, showWarnings = FALSE)
if (save_clean_trades) {
  dir.create(trades_dir, recursive = TRUE, showWarnings = FALSE)
}

message("Connecting to WRDS PostgreSQL as user '", wrds_user, "'.")
connect_args <- list(
  drv = RPostgres::Postgres(),
  host = "wrds-pgdata.wharton.upenn.edu",
  port = 9737,
  dbname = "wrds",
  sslmode = "require",
  user = wrds_user
)
wrds_password <- Sys.getenv("WRDS_PASSWORD", unset = "")
if (nzchar(wrds_password)) {
  connect_args$password <- wrds_password
}
wrds <- tryCatch(
  do.call(DBI::dbConnect, connect_args),
  error = function(e) {
    stop(
      paste(
        "Could not connect to WRDS PostgreSQL.",
        "Check your network/VPN, WRDS username, TAQ access, and ~/.pgpass or WRDS_PASSWORD.",
        paste("Underlying error:", conditionMessage(e)),
        sep = "\n"
      ),
      call. = FALSE
    )
  }
)
if (!DBI::dbIsValid(wrds)) {
  stop(
    paste(
      "WRDS PostgreSQL connection was created but is not valid.",
      "Check your WRDS credentials and try running the script via Rscript rather than source().",
      sep = "\n"
    ),
    call. = FALSE
  )
}
on.exit(DBI::dbDisconnect(wrds), add = TRUE)

start_key <- format(start_date, "%Y%m%d")
end_key <- format(end_date, "%Y%m%d")

available_tables <- DBI::dbGetQuery(
  wrds,
  paste0(
    "select table_name ",
    "from information_schema.tables ",
    "where table_schema = 'taqmsec' ",
    "and table_name ~ '^ctm_[0-9]{8}$' ",
    "and table_name >= ", DBI::dbQuoteString(wrds, paste0("ctm_", start_key)), " ",
    "and table_name <= ", DBI::dbQuoteString(wrds, paste0("ctm_", end_key)), " ",
    "order by table_name"
  )
)

dates <- sub("^ctm_", "", available_tables$table_name)
if (!is.na(max_days)) {
  dates <- head(dates, max_days)
}

message("Found ", length(dates), " TAQ trade tables in requested date range.")
if (length(dates) == 0 || dry_run) {
  if (length(dates) > 0) {
    print(utils::head(dates, 10))
    if (length(dates) > 10) {
      message("...")
      print(utils::tail(dates, 10))
    }
  }
  quit(status = 0)
}

daily_measures_path <- file.path(out_dir, sprintf("%s_daily_measures.csv", symbol))
daily_measures <- data.table()
if (file.exists(daily_measures_path) && !overwrite) {
  daily_measures <- fread(daily_measures_path)
}

download_one_day <- function(dd) {
  table_name <- paste0("ctm_", dd)
  date_label <- as.Date(dd, format = "%Y%m%d")
  bars_path <- file.path(bars_dir, sprintf("%s_%s_%dmin.csv.gz", symbol, dd, aggregate_minutes))
  trades_path <- file.path(trades_dir, sprintf("%s_%s_clean_trades.csv.gz", symbol, dd))

  if (!overwrite && file.exists(bars_path) &&
      (!save_clean_trades || file.exists(trades_path))) {
    message(dd, ": already exists, skipping.")
    return(NULL)
  }

  exchange_sql <- paste(DBI::dbQuoteString(wrds, exchanges), collapse = ", ")
  symbol_sql <- DBI::dbQuoteString(wrds, symbol)

  sql <- paste0(
    "select concat(date, ' ', time_m) as \"DT\", ",
    "ex as \"EX\", sym_root as \"SYM_ROOT\", sym_suffix as \"SYM_SUFFIX\", ",
    "price as \"PRICE\", size as \"SIZE\", tr_scond as \"COND\" ",
    "from taqmsec.", table_name, " ",
    "where ex in (", exchange_sql, ") ",
    "and sym_root = ", symbol_sql, " ",
    "and price != 0 ",
    "and tr_corr = '00'"
  )

  message(dd, ": querying WRDS.")
  trades <- as.data.table(DBI::dbGetQuery(wrds, sql))
  if (nrow(trades) == 0) {
    warning(dd, ": no trades returned for ", symbol, ".", call. = FALSE)
    return(data.table(
      date = date_label, symbol = symbol, n_intraday = 0L,
      open_taq = NA_real_, close_taq = NA_real_,
      rv = NA_real_, rskew = NA_real_, rkurt = NA_real_
    ))
  }

  trades[, DT := lubridate::ymd_hms(DT, tz = "UTC", quiet = TRUE)]
  trades <- trades[!is.na(DT)]

  cleaned <- trades |>
    highfrequency::exchangeHoursOnly() |>
    highfrequency::tradesCondition() |>
    highfrequency::selectExchange(exchanges) |>
    highfrequency::mergeTradesSameTimestamp() |>
    highfrequency::rmOutliersTrades()

  cleaned <- as.data.table(cleaned)
  if (nrow(cleaned) == 0) {
    warning(dd, ": no trades left after cleaning.", call. = FALSE)
    return(data.table(
      date = date_label, symbol = symbol, n_intraday = 0L,
      open_taq = NA_real_, close_taq = NA_real_,
      rv = NA_real_, rskew = NA_real_, rkurt = NA_real_
    ))
  }

  if (save_clean_trades) {
    fwrite(cleaned, trades_path)
  }

  bars <- as.data.table(highfrequency::aggregatePrice(cleaned, alignPeriod = aggregate_minutes))
  fwrite(bars, bars_path)

  bars[, ret := 100 * (log(PRICE) - shift(log(PRICE), type = "lag"))]
  returns <- bars[!is.na(ret), ret]
  data.table(
    date = date_label,
    symbol = symbol,
    n_intraday = nrow(cleaned),
    n_bars = nrow(bars),
    open_taq = bars$PRICE[1],
    close_taq = bars$PRICE[nrow(bars)],
    rv = sum(returns^2),
    rskew = if (length(returns) > 0) highfrequency::rSkew(returns) else NA_real_,
    rkurt = if (length(returns) > 0) highfrequency::rKurt(returns) else NA_real_
  )
}

for (dd in dates) {
  result <- tryCatch(
    download_one_day(dd),
    error = function(e) {
      warning(dd, ": ", conditionMessage(e), call. = FALSE)
      data.table(
        date = as.Date(dd, format = "%Y%m%d"),
        symbol = symbol,
        n_intraday = NA_integer_,
        n_bars = NA_integer_,
        open_taq = NA_real_,
        close_taq = NA_real_,
        rv = NA_real_,
        rskew = NA_real_,
        rkurt = NA_real_,
        error = conditionMessage(e)
      )
    }
  )

  if (!is.null(result)) {
    daily_measures <- rbindlist(list(daily_measures, result), fill = TRUE)
    setorder(daily_measures, date)
    daily_measures <- unique(daily_measures, by = c("date", "symbol"), fromLast = TRUE)
    fwrite(daily_measures, daily_measures_path)
  }
}

message("Done. Outputs written under: ", normalizePath(out_dir, mustWork = FALSE))
