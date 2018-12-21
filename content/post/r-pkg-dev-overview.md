+++
date = "2018-04-24"
title = "Package development in R - Overview"
+++

Creating an R package is as easy as typing:
```
package.skeleton(name = "YourPackageName")
```
As you might have guessed, this function creates the basic file and folder structure you need to create an R package. You will get:

```
YourPackageName/
    DESCRIPTION
    man/
    NAMESPACE
    R/
```
You can also use RStudio to create a package with `File > New Project ... > New Directory > Create R Package using devtools`. This is the way I actually prefer!

Before you continue, make sure you run `install.packages("devtools")` as we will be using this package a lot.

In the following few sections I will show you the essentials you need to build an R package. Hopefully, at the end of this post, you will feel confident enough to try it on your own. 

Working with packages requires a bit of an investment up-front, but the payoffs are huge, especially if you use RStudio. You will get:

- Near effortless unit testing with `testthat` (or as effortless as unit testing can be :),
- function and dataset documentation with `roxygen2` and
- most importantly: reproducibility.

We will cover all necessary aspects to build a package in sequence: 
## DESCRIPTION

This file contains, you guessed it, the description of your package. Among other things it specifies:
```
Package: Name
Type: Package
Title: What the package does (short line)
Version: 1.0
Date: 2018-04-24
Author: Who wrote it
Maintainer: Who to complain to <yourfault@somewhere.net>
Description: More about what it does (maybe more than one line)
License: What license is it under?
```

But most importantly, it also specifies which other packages your package depends on.

The `Imports` part specifies which packages are essential for your package to work, with version number if required:
```
Imports:
    data.table (>= 1.10.4),
    dbplyr
```

The `Suggests` part specifies which packages are nice to have:
```
Suggests:
    ggplot2
```

There is also the possibility to add packages to `Depends`, which differs from `Imports` in one crucial aspect:

- `Depends` loads packages into the Global Environment when the user uses `library(your-package)` while `Imports` does not.

Because naming conflicts become exponentially more likely the more packages you load, the best practice is to use `Imports`.

One way to add packages to your `DESCRIPTION` file is to list them there manually. My preferred way is to use:

```
devtools::use_package("package-to-add-to-DESCRIPTION-file-in-Imports-section")
```

## Man

`Man` is short for manual and this folder will contain all your function documentation. There are two possible ways to write documentation in R packages:

- The hard way, aka manually.
- The easy way, using the `roxygen2` package.

The easy way is, you guessed it, easy :) Writing function documentation works using tags:
```
#' Function caption here
#'
#' Function description here
#'
#' @param data
#' @param x
#' @return y
#' @import data.table
#' @importFrom dplyr `%>%`
my_function = function(data, x) {
    y = data[,.(sum_x = sum(x))]

    return(y)
}
```

As you can see, `@param` specifies all necessary parameters, which brings us already to the

## NAMESPACE
 `@import` and `@importFrom` are used to make other packages available in your package without having to use `pkg_name::fun_name`. This is the package-way of using `library()` with the added benefit that you can also import individual functions only (such as the pipe operator in the example above) using `@importFrom`. 

 > Never ever use `library(some-pkg-here)` in your package code!

You can now run `Ctrl+Shift+D` in RStudio to run `roxygen` and document your functions and generate the appropriate `NAMESPACE` entries automatically. 

I like to set RStudio to run `roxygen` everytime I build my package by ticking `Generate documentation with Roxygen` and specifying it in `Configure...`:

![run-roxygen-on-build][roxygen-on-build]

## R
The R folder is where all your scripts should go. There is one important caveat:

> The R folder cannot have subdirectories :(

So no Python-style nesting, I am afraid...

## Tests
One very important part is still missing: the `/tests/` folder. Run:
```
devtools::use_testthat()
```

This command will set you up to work with the `testthat` unit testing framework. Not coming from a software engineering background, I only did adhoc tests in the beginning mostly in the console to debug my code. Nothing automated at all. That caused two big problems:

1. Massive time waste making sure that everything still works as expected after code changes.
2. Never feeling quite sure if changing a function might lead to failures - especially if you do not remember your 'console' tests :)

Using `testhat` is super simple and while it does make sense in some cases to relax some parts of the [test-driven-development](https://en.wikipedia.org/wiki/Test-driven_development){:target="_blank"} framework in a data science setting (e.g. writing lots of tests for a feature that is probably not going to make it into the final model is quite time consuming), I cannot stress enought how important it is to properly unit test your code. You should even think about [unit testing your machine learning models](https://medium.com/@keeper6928/how-to-unit-test-machine-learning-code-57cf6fd81765){:target="_blank"}.

I will only give you a brief overview, but that should already cover 90% of all use cases. Unit tests have to be placed in placed in `/tests/testthat/` and the file name must start with `test_[your_function_name].R`. 

Every `test_file` contains something along the lines of:
```
library(testthat)

context("Description of your tests")

data_test = c(1,2,3)

test_that("test description", {
  expect_equal(fun(data_test),
               c(1,2,3)
          )
          })
```

You can run all your unit tests using `Crtl+Shift+T` in RStudio, which will show you a nice output with the number of tests passed and tests with errors.

## Some final tips for development

You can use `Crtl+Shift+L` to quickly load all of our functions into your R session to experiment without having to build the entire package.

To build the entire package run `Crtl+Shift+B`.

> Note that if you want RStudio to respect an `.Rprofile` file during the build process, you have to place the file on the same level as your package folder.

Building your package will also install it into your library if successful.

when you want to install your package including all dependencies, you can run:
```
devtools::install_deps(pkg = "/path/to/your/pkg/")
```


## Further reading
You can find additional information in:

- [R Packages](http://r-pkgs.had.co.nz/){:target="_blank"} from Hadley Wickham (if you never heard of Hadley before, his books and packages are amazing!).
- [Writing R extensions](https://cran.r-project.org/doc/manuals/r-release/R-exts.html){:target="_blank"}, the official guideline on CRAN.
- You might also be interested in reading about [semantic versioning](https://en.wikipedia.org/wiki/Software_versioning){:target="_blank"} or versioning more generally.


I hope you found this short post helpful!

[roxygen-on-build]: /img/rstudio-project-settings.PNG "RStudio Build Settings"