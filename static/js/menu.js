class Menu {
  create(data) {
  	// Display the game's name
  	let nameLabel = this.add.text(180, 80, 'Match-3', { font: '50px Arial', fill: '#000' });
    nameLabel.setOrigin(0.5, 0.5);

    // Display score, if any
    if (data.score > 0) {
      var scoreLabel = this.add.text(180, 200, 'score: ' + data.score, { font: '25px Arial', fill: '#000' });
      scoreLabel.setOrigin(0.5, 0.5);        
    }

    // Display how to start the game
    let startLabel = this.add.text(180, 320, 'click anywhere to start', { font: '25px Arial', fill: '#000' });
    startLabel.setOrigin(0.5, 0.5);
    this.tweens.add({
      targets: startLabel, 
      y: "-=20",
      duration: 200,
      hold: 500,
      repeatDelay: 500,
      yoyo: true,
      repeat: -1,
    });
  }

  update() {
  	// When we click
  	if (this.input.activePointer.isDown) {
      // Start the play scene
      this.scene.start('play');
  	}
  }
}
