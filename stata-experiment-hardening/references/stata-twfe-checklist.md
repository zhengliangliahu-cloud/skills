# Stata TWFE Checklist (Windows, reproducible)

## A. Pre-run contract
- Unit of analysis: firm-year panel.
- Main FE: firm FE + year FE.
- Main SE cluster: city (or thesis-approved level).
- Core treatment: `did_city` (or explicitly defined alternative).

## B. Path hardening
```powershell
subst X: "D:\parttime\税收柔性政策"
```
Use `X:/...` in all `.do` input/output paths.

## C. Stata bootstrap block
```stata
clear all
set more off
cap log close _all
log using "X:/analyse/logs/fe_twfe_run.log", replace text

import delimited "X:/data/analysis_data_en.csv", varnames(1) clear
* If explicit encoding causes issues, remove encoding() and retry.
```

## D. FE spec check block
```stata
egen firm_id = group(stkcd)
egen city_id = group(city)
egen year_id = group(year)
xtset firm_id year

* Main TWFE
xtreg long_term_ratio did_city i.year, fe vce(cluster city_id)
```

## E. Safe coefficient extractor
```stata
cap program drop extract_coef
program define extract_coef, rclass
    syntax , VAR(name)
    tempname b se t p
    scalar `b'  = _b[`var']
    scalar `se' = _se[`var']
    if (`se'==0 | missing(`se')) {
        return scalar b = `b'
        return scalar se = `se'
        return scalar t = .
        return scalar p = .
    }
    scalar `t' = `b'/`se'
    scalar `p' = 2*ttail(e(df_r), abs(`t'))
    return scalar b = `b'
    return scalar se = `se'
    return scalar t = `t'
    return scalar p = `p'
end
```

## F. Safe postfile pattern (avoid r() overwrite)
```stata
postfile p2 str8 model str20 core_var double coef t_stat str3 sig using "X:/analyse/tables/t2_tmp.dta", replace

quietly xtreg long_term_ratio did_city i.year, fe vce(cluster city_id)
quietly extract_coef, var(did_city)
local b = r(b)
local t = r(t)
local p = r(p)
local sig = cond(missing(`p'),"ns",cond(`p'<0.01,"***",cond(`p'<0.05,"**",cond(`p'<0.1,"*","ns"))))
post p2 ("col1") ("did_city") (`b') (`t') ("`sig'")

postclose p2
use "X:/analyse/tables/t2_tmp.dta", clear
export delimited using "X:/analyse/tables/Table2_Baseline.csv", replace
```

## G. Placebo extraction (permute-safe)
```stata
permute did_city _b[did_city], reps(1000) saving("X:/temp/placebo_results.dta", replace): ///
    xtreg long_term_ratio did_city size lev roa cash age float_ratio i.year, fe vce(cluster city_id)

use "X:/temp/placebo_results.dta", clear
ds _pm*
local plist `r(varlist)'
local pv : word 1 of `plist'
count if abs(`pv') >= abs(true_beta)
scalar p_placebo = r(N)/_N
```

## H. Treatment coding audit
```stata
* Example: verify 2020 pilot provinces
preserve
keep if year==2020
collapse (min) did (max) did_max=did, by(province)
list province did did_max
restore
```

## I. Delivery sync checklist
- Export canonical outputs to `X:/analyse/tables` and `X:/analyse/figures`.
- Sync to mirrored delivery folders after successful run.
- Update interpretation docs only after table timestamps are refreshed.

## J. Interpretation discipline
- Treat TWFE baseline as the main inference.
- Treat linear trend replacement as sensitivity only.
- Avoid claiming effect significance if only sensitivity columns are significant.
