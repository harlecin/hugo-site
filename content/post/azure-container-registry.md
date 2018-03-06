+++
date = "2018-03-05"
title = "Azure Container Registry"
+++

To push an image to the Azure Container Registry, first go to your Azure Container Registry service in the Azure portal.

In the 'Overview' section you can find a field called 'Login server'. Jot down this address.
![Screenshot Azure Portal - Container Services][azure-portal-container-services]

In a next step, login to your registry with:
```
docker login <your-login-server-address-here>
```

You can find your access credentials under 'Settings/Access Keys'.

After you logged in successfully, you tag the image using:
```
docker tag <source_image[:TAG]> <your-login-server-address-here>/<target_image[:TAG]>
```
Then push the image to the registry like so:
```
docker push <your-login-server-address-here>/<target_image[:TAG]>
```
And we are done:) You can now pull your image using `docker pull`.

[azure-portal-container-services]: /img/az-container-services.PNG "Screenshot Azure Portal - Container Services"