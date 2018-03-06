+++
date = "2018-03-05"
title = "Azure Container Registry - Quick Start Guide"
+++

Azure Container Registry is the Microsoft equivalent to privat Dockerhub repositories. First, I will show you how to quickly push an image to the registry. In a second step, I will cover how to manage your images (grouping, updating, deleting, etc) and in a last step, I will briefly dive into how you can authenticate with your registry.

## Quick start
To push a docker image to the Azure Container Registry, first go to your Azure Container Registry service in the Azure portal.

In the 'Overview' section you can find a field called 'Login server'. Jot down this address.  

![Screenshot Azure Portal - Container Services][azure-portal-container-services]

In a next step, login to your registry with:
```
docker login your-login-server-address-here
```
You will see a command prompt asking you for user name and password. You can find your access credentials under 'Settings/Access Keys'.

After you logged in successfully, you tag the image using:
```
docker tag source_image[:TAG] your-login-server-address-here/target_image[:TAG]
```
Then push the image to the registry like so:
```
docker push your-login-server-address-here/target_image[:TAG]
```
And we are done:) You can now pull your image using `docker pull`.


## Connecting with ActiveDirectory and PowerShell
On Windows, using Powershell is probably one of the easiest and most powerful ways to manage your Azure resources (including the container registry). The preferred method to install the cmdlet is to use PowerShellGet and pull it directly from the PowerShell Gallery. So first, we need to check if PowerShellGet is available:
```
Get-Module -Name PowerShellGet -ListAvailable | Select-Object -Property Name,Version,Path
```

You should see PowerShellGet, a version number and a path, if it is installed. Next, run:
```
Install-Module -Name AzureRM -AllowClobber
```
If you run this command for the first time, PowerShell will ask you if you want to trust this repo. Answer 'yes' and continue.


After the module is installed, you need to import it before you can use it using (non-elevated session is sufficient, i.e. no admin rights are necessary):
```
Import-Module -Name AzureRM
```

Now, we are ready to log in to our subscription:
```
Login-AzureRmAccount
```
You should see a pop-up window asking for your username and password.  

> Note: Powershell Core v6.0.0 crashed when trying to open the login window, so I relied on the 'old' Powershell instead.

Now let's get our login credentials and save them to a variable:
```
$resource_group = "your-azure-resource-group"
$registry_name = "your-registry-name"
$registry = Get-AzureRmContainerRegistry -ResourceGroupName $registry_group -Name $registry_name
$creds = Get-AzureRmContainerRegistryCredential -Registry $registry
```

You can now login to your Container registry with:
```
docker login $registry.LoginServer -u $creds.Username -p $creds.Password
```
When you get 'Login Succeed' you can throw your hands up in the air:)

As of the time of this writing, there does not seem to be an option to list all containers or delete them.

## Connecting using Azure CLI
You can also use the Azure CLI tool in Powershell to manage your repository (and Azure ressources more generally). You can check if Azure CLI is installed by running:

```
az --version
```

If you do not have Azure CLI already installed, [download](https://azurecliprod.blob.core.windows.net/msi/azure-cli-latest.msi) it and run the installer. You might have to add `C:\Program Files (x86)\Microsoft SDKs\Azure\CLI2\wbin` to your path so that Powershell finds the cmdlet. 

First, we need to connect to our Azure account:
```
az login
```

If you get an SSL "bad handshake" error, "tls_process_server_certificates, certificate verify failed" I am afraid I currently do not know how to fix that, but I am working on it.

## Managing images
Every container registry contains 1:n repositories that are used to group container images together (e.g. by project).

Repositories are defined by using slashes `/` as follows:  

- `your-login-server-address-here/target_image[:TAG]` is a top-level image
- `your-login-server-address-here/project_name/target_image[:TAG]` is a project specific image
- `your-login-server-address-here/project_name/sub_project/target_image[:TAG]` is an image in a sub-project of the main project

You can view all your images by navigating to your registry in the Azure Portal and clicking on the 'Repository' tab. You can also start containers directly from there.

## Best practices
- https://docs.microsoft.com/en-us/azure/container-registry/container-registry-best-practices



[azure-portal-container-services]: /img/az-container-services.PNG "Screenshot Azure Portal - Container Services"