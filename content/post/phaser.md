+++
date = "2023-11-11"
title = "Game Dev, Javascript and Deno"
+++

I have been dabbling in Javascript every once in a while over the last few years, but I just never got myself to like the language and the ecosystem a lot. While I understood that Javascript and the npm ecosystem had a lot to offer, I just did not know where to get started, because it felt like everytime I sat down to start learning again, the entire ecosystem had already moved on. Also Javascript just seemed to me like a language that was bolted together vs. carefully engineered. 

However, [den0](https://deno.com/) came around and I do have to say I was/am very intrigued. Deno offered a batteries included approach, a secure-by-default runtime, Typescript by default and super easy deployment. I played around with Deno's webframe work Fresh and I have to say, I really like it! While deno is steadily improving Node.js interoperability it is sadly not there yet and a lot of libraries that I would need for deno to be useful in my day job don't exist yet (e.g. oracle-drivers: oracle is still alive and kicking in the large enterprise database world ...). 

Nevertheless, I see a lot of potential for deno and that made me try Javascript again. This time I decided to start with something less busineesy and more fun and I decided to learn Javascript by programming web games in [phaser3](https://phaser.io/). At first I also took a brief look at Unity, mainly because of C# vs. Javascript and at [playcanvas](https://phaser.io/) another Javascript game engine that has an excellent editor for 3d games. I decided to stick with `phaser` mainly, because I grew up with a Gameboy and I love casual 2d games, which is what `phaser` excells at.

Getting started with `phaser` is also very easy, you can gradually easy into setting up the complete Javascript development stack. If you are interested, checkout the great tutorial on the official website. At the moment I am migrating my `phaser` projects to [vite](https://vitejs.dev/), because it comes with a lot of nice features that make development more pleasant. I will write more about my migration in another post (which will hopefully not sit on the shelf for ages like my still only partially finished raytracing blog, where I need to generate nice visuals. Maybe if I wait a bit longer, Midjourney can also do mathematical charts ^_^).

After dabbling a bit with different `phaser` tutorials I bought the book 'Make 2d Games in Javascript with Phaser' by Thomas Palef to learn how to create games in a more professional manner. Thomas' book is really amazing, he takes you all the way from the very basics to a fully functional game that also works on mobile. He also includes additional game templates that you can easily customize. Worth every cent in my mind, really a very good resource. I have no affiliation whatsoever, just a very happy customer. You can buy his book [here](https://thomaspalef.gumroad.com/l/make-2d-games)

Below you can find a slightly modded match-3 game using Thomas' template code. I plan to extend it in the future and include additional mechanics, but I think it is very fun already in this simple version:

<head>
<meta charset="utf-8" />

<script src="https://harlecin.netlify.app/js/phaser.min.js"></script> 
<script src="https://harlecin.netlify.app/js/load.js"></script>
<script src="https://harlecin.netlify.app/js/menu.js"></script>
<script src="https://harlecin.netlify.app/js/play.js"></script>
<script src="https://harlecin.netlify.app/js/game.js"></script>
</head>
<body>
<div id="game"></div>
</body>
