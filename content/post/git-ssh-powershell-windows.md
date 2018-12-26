+++
date = "2018-12-24"
title = "Git & SSH with Powershell Core"
+++

In this post I want to give a quick outline of how to setup Powershell Core (Microsoft's cross-platfrom version of Powershell) to work with `git` and `ssh`.

While you can simply install [Git for Windows](https://git-scm.com/download/win) and work with Git Bash, personally I quite like Powershell Core, because it is more tightly integrated with Windows and Azure. I will not cover working with CMD, because in my personal opinion, CMD offers, to put it mildly, a suboptimal user experience ...

So, let's get started:

- Install [Git for Windows](https://git-scm.com/download/win)
- Install [Powershell Core](https://github.com/PowerShell/PowerShell)
- Run Powershell as Admin with:
`Set-ExecutionPolicy -Scope LocalMachine -ExecutionPolicy RemoteSigned -Force` 

This will allow all users to execute scripts that have been remotely signed, i.e. are from the web. Optionally, you can also use `"-Scope CurrentUser"` if you only want to enable remotely signed scripts for your user account.

- Open Powershell and type `git` to check that it is on your PATH and do the same with `ssh`. If it is not on your PATH, you need to add it before you continue.
- Setup `Posh-Git` by running the following in Powershell:

```
Set-PSRepository -Name PSGallery -InstallationPolicy Trusted
PowerShellGet\Install-Module posh-git -Scope CurrentUser -AllowPrerelease -Force

## Update an existing version:
PowerShellGet\Update-Module posh-git

## Add PoshGit to all PowerShell hosts (console, ISE, etc)
Add-PoshGitToProfile -AllHosts
```

Now that we have Posh-Git up and running, let's generate a public/private key-pair:

- Open Powershell and run `ssh-keygen -t rsa -b 4096 -C "your_email@example.com"` and press enter to save to the default location. You can set a password as well.
- Now you need to add your key to `ssh-agent`. I used Git Bash to start `ssh-agent` with `eval $(ssh-agent -s)`, because Windows 10 now also ships with `ssh` and Git wants to use its own bundled ssh binaries, while posh-git starts the Windows ssh binaries (see [Windows 10 version 1803 broke my git SSH](https://adamralph.com/2018/05/15/windows-10-version-1803-broke-my-git-ssh/) if you want to use the ssh binaries shipped with Windows instead of with Git)
- Run `ssh-add ~/.ssh/id_rsa` to add your key to `ssh-agent`.

Now you should be ready to use `git`+`ssh` with Powershell:)