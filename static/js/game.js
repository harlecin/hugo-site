let game = new Phaser.Game({
  width: 360,
  height: 400, 
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH
  },
  transparent: true,
  physics: { default: 'arcade' },
  parent: 'game', 
});

game.scene.add('load', Load);
game.scene.add('menu', Menu);
game.scene.add('play', Play);

game.scene.start('load');
