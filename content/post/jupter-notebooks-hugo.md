
+++
date = "2018-11-20"
title = "Blogging with Hugo and Jupyter"
+++

I really love blogging with Hugo+Blogdown, but unfortunately Blogdown is still mostly restricted to R (although Python is now also possible using the `reticulate` package).

Jupyter offers a great literate programming environment for multiple languages and so being able to publish Jupyter notebooks as Hugo blogposts would be a huge plus. 

I have been looking for a way to incorporate Jupyter notebooks into my blogging workflow for a while now and I narrowed my options down to the following:

- `hugo_jupyter` Python package (see [here](http://journalpanic.com/post/blogging-with-hugo-and-jupyter-notebooks/) for a short tutorial)
- Writing plain vanilla markdown without code output
- Converting Jupyter notebooks to markdown using `nbconvert`

Today I decided to give `nbconvert` a go, because I did not want dive into setting up additional libraries.

As it turns out, using `nbconvert` to convert Jupyter notebooks to .md files is actually really straightforward.

My current setup is:

```
    blog-folder/
        jupyter-notebooks/
        other-folders/
```

To create a blogpost all you have to do is `cd` into the directory that contains your notebooks and run:

```
jupyter nbconvert --to markdown <notebook-name>.ipynb
```


```
## This gets rendered as code:
print('test')
```

    test
    

Now let's try some graphs:


```
from plotnine import *
from plotnine.data import *
import warnings
warnings.filterwarnings('ignore')
```


```
mtcars.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>mpg</th>
      <th>cyl</th>
      <th>disp</th>
      <th>hp</th>
      <th>drat</th>
      <th>wt</th>
      <th>qsec</th>
      <th>vs</th>
      <th>am</th>
      <th>gear</th>
      <th>carb</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Mazda RX4</td>
      <td>21.0</td>
      <td>6</td>
      <td>160.0</td>
      <td>110</td>
      <td>3.90</td>
      <td>2.620</td>
      <td>16.46</td>
      <td>0</td>
      <td>1</td>
      <td>4</td>
      <td>4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Mazda RX4 Wag</td>
      <td>21.0</td>
      <td>6</td>
      <td>160.0</td>
      <td>110</td>
      <td>3.90</td>
      <td>2.875</td>
      <td>17.02</td>
      <td>0</td>
      <td>1</td>
      <td>4</td>
      <td>4</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Datsun 710</td>
      <td>22.8</td>
      <td>4</td>
      <td>108.0</td>
      <td>93</td>
      <td>3.85</td>
      <td>2.320</td>
      <td>18.61</td>
      <td>1</td>
      <td>1</td>
      <td>4</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Hornet 4 Drive</td>
      <td>21.4</td>
      <td>6</td>
      <td>258.0</td>
      <td>110</td>
      <td>3.08</td>
      <td>3.215</td>
      <td>19.44</td>
      <td>1</td>
      <td>0</td>
      <td>3</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Hornet Sportabout</td>
      <td>18.7</td>
      <td>8</td>
      <td>360.0</td>
      <td>175</td>
      <td>3.15</td>
      <td>3.440</td>
      <td>17.02</td>
      <td>0</td>
      <td>0</td>
      <td>3</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
</div>




```
(ggplot(mtcars, aes(x='disp',y='mpg'))
    + geom_point()
    + geom_smooth()
    + ggtitle('A graph')
)
```


![png](/img/jupter-notebooks-hugo_files/jupter-notebooks-hugo_5_0.png)





    <ggplot: (-9223371921876142392)>



Running `nbconvert` will put all images in a folder next to your jupyter notebook. So we need to copy the pic folder to `/static/` in our hugo directory and fix the links.

That's it more or less:) When I find the time, I will look into a more automated setup. Hope you found this post interesting and happy blogging!
