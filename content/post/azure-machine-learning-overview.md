+++
date = "2018-02-27"
title = "Azure Machine Learning Services - Overview"
+++

Microsoft's cloud plattform Azure has grown rapidly over the past few years and is adding features at an enormous pace. In this post, I am going to explore and compare different ways to do machine learning in Azure.  In particular, I am going to focus on the following services:

- Azure Machine Learning Studio
- Azure Machine Learning Services
- Azure Container Services

For each service I will cover features offered, deployment options, pricing model, target-users and availability regions as of Feburary 27, 2018. 

At of the post I will include a short checklist with important points (imo) to consider before choosing a specific service.

## Azure Machine Learning Studio
Azure Machine Learning Studio is perhaps the easiest option to experiment and deploy a machine learning solution. It provides a browser-based drag-and-drop interface that allows users to create a machine learning pipeline by connecting various preconfigured elements:

![screen shot azure ml studio][azure-ml-studio]

Moreover, it allows more advanced users to include R and Python scripts as well. The final model can be published as a webservice. The service includes various templates for anomaly detection, customer analysis etc. There is also an R package available on CRAN called [AzureML](https://CRAN.R-project.org/package=AzureML) that allows you to:

- Connect to your Azure ML workspace
- Up/download datasets
- Publish/consume/update Azure ML webservices

You can also connect to AzureML using Python. Just run `pip install azureml` and you are ready to go:) More detailed documentation is available on [Github](https://github.com/Azure/Azure-MachineLearning-ClientLibrary-Python).

The pricing model has two components:

- Development: FREE and STANDARD tier (about € 8.5 per user/month + € 0.85 per compute hour) 
- Deployment: free for DEV/TEST and about €85 for STANDARD S1, €850 for STANDARD S2 and €8500 for STANDARD S3 

which give you a certain number of compute hours, transactions and number of web services running per month. For more details check the [Azure pricing calculator](https://azure.microsoft.com/en-us/pricing/)

West and North Europe are both offered as availability regions. The target-user group for this service covers both data analysts and data scientists.

## Azure Machine Learning Services
Microsoft markets Azure ML Serives (not Studio!) as an 'end-to-end, scalable, trusted platform', which begs the question why someone would want to use an untrusted platform:) AzureML Services consists of the following components:

A desktop data-science development-environment called:
- Workbench 

to manage:
- Experimentation service
- Model management

You can also use an addin for Visual Studio Code:
- Visual Studio Code Tools for AI

Last, but not least, there are:
- AI Toolkit for Azure IoT Edge
- MMLSpark

AzureML Workbench runs on W10, WS2016, macOS Sierra or High Sierra only. Azure ML Workbench will also force you to install Python 3.5, Miniconda, Azure ML Data Profile, Azure ML CLI and a couple of other dependencies such as Jupyter. So it seems that changing the Python interpreter is not possible at the moment. AzureML Workbench does not support R at the time of writing.   

In order to use AzureML Workbench, you need to create an Azure Experimentation service and Model management service. AzureML Workbench is then used to connect to these services. 

A couple of notes before you go ahead an install the Workbench:
> MS warns that installation can take quite long (around 30min) and you should download the installer to disk and launch it from there and NOT from your browser widget!

I only saw the second warning after launching the installer from the browser and after about 10min it does indeed throw an error and the installation terminates, so that is that:)

After the install is complete, you need to sign in with your Azure credentials. By default Workbench will choose the first(!) Experimentation account it finds in your subscription. You can change the Experimentation account afterwards though.
## Data science plattform checklist

The following checklist is by no means complete, but maybe helpful in choosing data science plattforms:

- Availibility region: Is my company restricted to certain regions (e.g. Germany, West Europe, etc) and is the service available in this region?
- Does the service offer all necessary libraries for my project and if not, is there an option to install them?
- Does the service support the appropriate runtime of R/Python I want to use?
- Does the service provide public endpoints (i.e. can it be reached by a public ip address) and if yes, does my corporate security policy allow such services?
- Is the service GDPR compliant? If in doubt, check with your companies security department and/or the plattform vendor.
- How easy is it to port an existing data science model to a different plattform (e.g. from Azure to AWS or back)?
- What kind of load am I expecting and can the service scale appropriately?
- What does pricing look like for different usage scenarios?


[azure-ml-studio]: ../../data/azure-machine-learning-studio.jpg "Azure Machine Learning Studio"