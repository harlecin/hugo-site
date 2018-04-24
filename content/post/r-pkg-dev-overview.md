+++
date = "2018-04-24"
title = "Package development in R - Overview"
+++


Using devtools + roxygen:

- Write to namespace:
```
#' Function caption
#'
#' Function description
#'
#' @param data
#' @param x
#' @return y
#' @import data.table
#' @importFrom dplyr `%>%`
```

```
devtools::use_testthat()
```

Add package to DESCRIPTION file
```
devtools::use_package("<pkg_name>")
```