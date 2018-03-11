+++
date = "2018-03-05"
title = "Azure Container Registry - Quick Start Guide"
+++

Azure Container Registry is the Microsoft equivalent to private Dockerhub repositories. First, I will show you how to quickly push an image to Azure Container Registry. In a second step, I will cover how to manage your registries and repositories using the PowerShell cmdlet `AzureRM` as well as the `Azure CLI`.

## Quick start
To push a docker image to Azure Container Registry, first go to your Azure Container Registry service in the Azure portal.

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

## Managing images
Every container registry contains 1:n repositories that are used to group container images together (e.g. by project).

Repositories are defined by using slashes `/` as follows:  

- `your-login-server-address-here/target_image[:TAG]` is a top-level image
- `your-login-server-address-here/project_name/target_image[:TAG]` is a project specific image
- `your-login-server-address-here/project_name/sub_project/target_image[:TAG]` is an image in a sub-project of the main project

You can view all your images by navigating to your registry in the Azure Portal and clicking on the 'Repository' tab. You can also start containers directly from there.

## Connecting with ActiveDirectory and PowerShell
On Windows using Powershell is probably one of the easiest and most powerful ways to manage your Azure resources (including the container registry). 

You can install the `AzureRm` cmdlet to manage your container registry. `AzureRm` is primarily focused on managing Azure services from a sysadmin perspective and provides mainly functions to create and change Azures services. I have not yet found a way to e.g. delete repositories in an Azure registry or list all repositories in a given registry. A more powerful solution is the Azure CLI (see next section).

The preferred method to install the cmdlet is to use `PowerShellGet` and pull it directly from the PowerShell Gallery. So first, we need to check if `PowerShellGet` is available:
```
Get-Module -Name PowerShellGet -ListAvailable | Select-Object -Property Name,Version,Path
```

You should see `PowerShellGet`, a version number and a path, if it is installed. Next, run:
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

**Note**: Powershell Core v6.0.0 crashed when trying to open the login window, so I relied on the 'old' Windows Powershell instead.

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
You should get a 'Login succeeded' message.

## Connecting using Active Directory and Azure CLI 
You can also use the Azure CLI tool in Powershell to manage your repository (and Azure resources more generally). You can check if Azure CLI is installed by running:

```
az --version
```

If you do not have Azure CLI already installed, [download](https://azurecliprod.blob.core.windows.net/msi/azure-cli-latest.msi) it and run the installer. You might have to add `C:\Program Files (x86)\Microsoft SDKs\Azure\CLI2\wbin` to your path so that Powershell finds the cmdlet. 

First, we need to connect to our Azure account:
```
az login
```

Follow the instructions in your console to login. If you get an SSL error check if your are using self-signed certificates. 

You can find an overview of the functionality provided by Azure CLI [here](https://docs.microsoft.com/en-us/cli/azure/). A few commands I find quite useful are provided below. Please be careful to check if you operate on an entire **registry** or on **repositories** in a registry!

- `az acr list -g your_resource_group -o table` to list all container services in a table for a specific resource group
- `az acr delete --name [--resource-group]` to delete a container registry
- `az acr repository delete --name your_registry --repository repo_to_delete [--resource-group your_resource_group][--tag tag_to_delete]` to delete a repository in your container registry with a specific tag. If you omit the tag, the entire repo is deleted 
- `az acr repository list` to show all images in a given 

You can find more commands [here](https://docs.microsoft.com/en-us/cli/azure/acr/repository?view=azure-cli-latest#delete).





[azure-portal-container-services]: /img/az-container-services.PNG "Screenshot Azure Portal - Container Services"