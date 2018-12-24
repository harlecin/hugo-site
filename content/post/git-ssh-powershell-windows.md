+++
date = "2018-12-24"
title = "Git & SSH with Powershell Core"
+++

In this post I want to give a quick outline of how to setup Powershell Core (Microsoft's cross-platfrom version of Powershell) to work with `git` and `ssh`.

While you can simply install [Git for Windows](https://git-scm.com/download/win) and work with Git Bash, personally I quite like Powershell Core, because it is more tightly integrated with Windows and Azure. I will not go into working with CMD, because in my personal opinion, CMD offers, to put it mildly,a a suboptimal user experience ...

So, let's get started:

1) Install [Git for Windows](https://git-scm.com/download/win)
2) Install [Powershell Core](https://github.com/PowerShell/PowerShell)
3) Run Powershell as Admin with:
`Set-ExecutionPolicy -Scope LocalMachine -ExecutionPolicy RemoteSigned -Force` 

This will allow all users to execute scripts that have been remotely signed, i.e. are from the web. Optionally, you can also use `"-Scope CurrentUser"` if you only want to enable remotely signed scripts for your user account.

4) Open Powershell and type `git` to check that it is on your PATH and do the same with `ssh`. If it is not on your PATH, you need to add it before you continue.

5) Install `Git-Posh`

Now that we have Posh-Git up and running, let's 