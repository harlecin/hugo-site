class Load {
  preload() {
    // Load all assets
    this.load.spritesheet('dot', 'assets/dot.png', { 
      frameWidth: 50, frameHeight: 49.75
    });
    this.load.audio('click', ['assets/click.ogg', 'assets/click.mp3']);

    // Loading label
    this.loadLabel = this.add.text(180, 200, 'loading\n0%', { font: '30px Arial', fill: '#fff', align: 'center' });
    this.loadLabel.setOrigin(0.5, 0.5);
    this.load.on('progress', this.progress, this);
  }

  progress(value) {
    // Update loading progress
    let percentage = Math.round(value * 100) + '%';
    this.loadLabel.setText('loading\n' + percentage);
  }

  create() {
    // Start the menu scene
    this.scene.start('menu');
  }
}
