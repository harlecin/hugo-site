+++
date = "2024-06-09"
title = "Creating a Phaser3 Game with Vite and Typescript"
+++

As promised in a previous post, finally a follow-up that goes into setting up a Phaser3 project with [`vite`](https://vitejs.dev/) and Typescript.

As of January 18th this year, you can also download a fully ready Vite template from [phaser.io](https://vitejs.dev/). You can find the template on Github at [this link](https://github.com/phaserjs/template-vite).

But before we start, maybe let's answer the following question: Why bother?

For me personally, I started out coding Phaser games using just plain js and html files and used `npx http-server -a 127.0.0.1 -c-1` to run a local development server. While that works, `vite` offers a couple of really nice perks for game development:

- Hot Module Replacement when your code changes
- Supports TypeScript, JSX and CSS out-of-the-box
- Easy way to create production builds when you are done with development

## Setup
Getting started with `vite` is super easy. Assuming you have `node.js` already installed, simply run `npm create vite@latest` and follow the prompts. Note for people who are new to the npm ecosystem: `npm create` is a shorthand for `npx create-<package-name>`. 

I recommend to go with the TypeScript template and allow JavaScript by adding the following snippet to your `tsconfig.json`:
```
"compilerOptions": {
    "allowJs": true,
```
This way, you can migrate to TypeScript at your own pace.

Now, let's install phaser by running: `npm install phaser`

Then run `npm run dev` to get started :)

## Phaser HelloWorld
By running `npm create vite@latest` and selecting framework "Vanilla" and variant "TypeScript", you will get the following project setup for you:
```
public/
    vite.svg
src/
    counter.ts
    main.ts
    style.css
    typescript.svg
    vite-env.d.ts
.gitignore
index.html
package.json
tsconfig.json
```
Now let's delete `counter.ts`, `style.css`, `typescript.svg` and `vite.svg`. Afterwards, add `HelloWorld.js` to `src/`.

Edit `tsconfig.json` as shown in the previous chapter to allow JavaScript in your project. 

Replace the code in `main.ts` with this:
```
import Phaser from 'phaser'

import HelloWorldScene from './HelloWorld'

const config = {
	type: Phaser.AUTO,
	parent: 'app',
	width: 800,
	height: 600,
	physics: {
		default: 'arcade',
		arcade: {
			gravity: { y: 200 },
		},
	},
	scene: [HelloWorldScene],
}

export default new Phaser.Game(config)
```

Add the following code to `HelloWorld.js`:
```
import Phaser from 'phaser'

export default class HelloWorldScene extends Phaser.Scene {
	constructor() {
		super('hello-world')
	}

	preload() {
		this.load.setBaseURL('https://labs.phaser.io')

		this.load.image('sky', 'assets/skies/space3.png')
		this.load.image('logo', 'assets/sprites/phaser3-logo.png')
		this.load.image('red', 'assets/particles/red.png')
	}

	create() {
		this.add.image(400, 300, 'sky')

		const particles = this.add.particles('red')

		const emitter = this.add.particles(0,0, "red", {
            speed: 100,
            scale: {start: 1, end: 0},
            blendMode: 'ADD'
        });

		const logo = this.physics.add.image(400, 100, 'logo')

		logo.setVelocity(400, 200)
		logo.setBounce(1, 1)
		logo.setCollideWorldBounds(true)

		emitter.startFollow(logo)
	}
}
```
Replace the code in `index.html` with the following and you are done:
```
<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
	<title>My Phaser 3 Game</title>
</head>

<body>
	<div id="app"></div>
	<script type="module" src="src/main.ts"></script>
</body>

</html>
```

Run `npm run dev` and you should see the Phaser HelloWorld setup.

## Deploying
After you are happy with your game, run `npm run build` and your game code will be bundled into a single file and together with all static assets saved to `dist/`.

Now simply upload all code in `dist/` to a public facing webserver.