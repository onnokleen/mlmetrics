#!/bin/zsh

set -euo pipefail

for source_file in ./*.qmd ./*.md; do
  [[ -e "$source_file" ]] || continue
  base_name=${source_file##./}
  base_name=${base_name:r}
  rm -f "./${base_name}.html"
done

rm -rf ./site_libs