#!/bin/bash
# Migrate result/abstraction dirs to match new bottom-up family naming.
# Run from repo root. Idempotent — skips if target already exists.
set -e
cd "$(dirname "$0")/.."

rename_dir() {
  local base="$1" old="$2" new="$3"
  if [ -d "$base/$old" ] && [ ! -d "$base/$new" ]; then
    echo "  mv $base/$old → $base/$new"
    mv "$base/$old" "$base/$new"
  elif [ -d "$base/$old" ] && [ -d "$base/$new" ]; then
    echo "  SKIP $base/$old (target $new already exists)"
  fi
}

echo "=== Renaming result dirs ==="
rename_dir results agastha-inc--agastha agastha-inc--agastha-enterprise-healthcare-software
rename_dir results athenahealth-inc--athenapractice athenahealth-inc--athenapractice-flow
rename_dir results nextech--nextech-select nextech--nextech-select-nexcloud
rename_dir results flatiron-health-and-others-27--oncoemr flatiron-health--oncoemr
rename_dir results net-health-and-others-26--net-health-woundexpert net-health--net-health-woundexpert
rename_dir results varian-medical-systems--aria varian-medical-systems--aria-core

echo "=== Renaming abstraction dirs ==="
rename_dir abstraction nextech--nextech-select nextech--nextech-select-nexcloud
rename_dir abstraction varian-medical-systems--aria varian-medical-systems--aria-core

echo "=== E*HealthLine merge (two products → one family) ==="
EHL_OLD_CARE="results/e-healthline-com-inc--care-integrated-hospital-information-management-system"
EHL_OLD_PHOENIX="results/e-healthline-com-inc--phoenix-integrated-electronic-health-records"
EHL_NEW="results/e-healthline-com-inc--e-healthline-ehr"
if [ -d "$EHL_OLD_CARE" ] && [ ! -d "$EHL_NEW" ]; then
  echo "  mv $EHL_OLD_CARE → $EHL_NEW (keeping CARE results as base)"
  mv "$EHL_OLD_CARE" "$EHL_NEW"
  if [ -d "$EHL_OLD_PHOENIX" ]; then
    echo "  rm -rf $EHL_OLD_PHOENIX (merged into new family)"
    rm -rf "$EHL_OLD_PHOENIX"
  fi
fi
for abs_old in \
  "abstraction/e-healthline-com-inc--care-integrated-hospital-information-management-system" \
  "abstraction/e-healthline-com-inc--phoenix-integrated-electronic-health-records"; do
  ABS_NEW="abstraction/e-healthline-com-inc--e-healthline-ehr"
  if [ -d "$abs_old" ] && [ ! -d "$ABS_NEW" ]; then
    echo "  mv $abs_old → $ABS_NEW"
    mv "$abs_old" "$ABS_NEW"
  elif [ -d "$abs_old" ] && [ -d "$ABS_NEW" ]; then
    echo "  rm -rf $abs_old (merged)"
    rm -rf "$abs_old"
  fi
done

echo "=== Done ==="
