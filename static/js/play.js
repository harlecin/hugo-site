/*

Here are the main steps of this game:

1- When the user clicks, call clicked()
2- Select the dot below the cursor: findClickedDot()
3- Select all adjacent dots to the clicked dot: selectDots()
3- Kill all the selcted dots: removeSelectedDots()
4- Update score and labels: updateScore()
5- Refill the world with dots: refillDots()

*/

class Play {
  create() { 
    // Create the dots group
    this.dots = this.physics.add.group();

    // Score label
    this.scoreLabel = this.add.text(15, 15, 'score: 0', { font: '18px Arial', fill: '#000' });

    // Number of moves left before the game ends
    this.moveLabel = this.add.text(345, 15, 'moves: 10', { font: '18px Arial', fill: '#000' });
    this.moveLabel.setOrigin(1, 0);

    // Various variables
    this.gridSize = 7;
    this.tileSize = 50;
    this.dotsSelected = 0;
    this.score = 0;
    this.moveCount = 10;
    this.clickSound = this.sound.add('click');

    // Fill the world with dots
    this.initWorld();
  }

  // This is the main function of the game
  // Called when the user clicks on a dot
  clicked() {
    // If some dots are already selected, do nothing
    if (this.dotsSelected !== 0) {
      return;
    }

    // Get the dot that is below the pointer
    let dot = this.findClickedDot();

    // Set 'dot.selected = true' to all the dots that should be removed
    this.selectDots(dot.i, dot.j, dot.frame);

    // Remove the dots that are selcted
    this.removeSelectedDots();

    // Update score
    this.updateScore();

    // Once the dots finish disapearing, refill the world with dots
    this.time.addEvent({
      delay: 300,  
      callback: () => this.refillDots(),
    });
  }

  // Fill the world with dots
  initWorld() {
    // Go through the grid (7x7)
    for (let i = 0; i < this.gridSize; i++) {
      for (let j = 0; j < this.gridSize; j++) {
        // Create a dot at each spot
        this.addDot(i, j);	
      }
    }	
  }

  // Add a new dot at the i, j position
  addDot(i, j) {
    // Retrive a dead dot from the group
    let dot = this.dots.create(30 + i * 50, 70 + j * 50, 'dot');

    // Handle clicks
    dot.setInteractive({ useHandCursor: true });
    dot.on('pointerdown', this.clicked, this)

    // Set a random frame
    dot.setFrame(Phaser.Math.RND.between(0, 3));

    // Add custom parameters to the dot
    dot.i = i;
    dot.j = j;
    dot.selected = false;

    // Tween
    dot.setScale(0, 0);
    this.tweens.add({
      targets: dot, 
      scale: 1,
      duration: 200, 
    });
  }

  // Return the dot that was clicked by the pointer
  findClickedDot() {
    let x = this.input.activePointer.x;
    let y = this.input.activePointer.y;

    // Convert the x, y point into i, j value
    let i = Math.floor((x - 30 + 25) / this.tileSize);
    let j = Math.floor((y - 70 + 25) / this.tileSize);

    return this.getDot(i, j);
  }

  // Select adjacent dots to the i, j dot if they have the same frame
  selectDots(i, j, frame) {
    // Get the corresponding dot
    let dot = this.getDot(i, j);
    if (!dot) {
      return;
    }

    // If the dot matches the color we are looking for (the same frame)
    if (dot.frame === frame && !dot.selected) {
      // Then select the dot
      dot.selected = true;
      this.dotsSelected += 1;

      // And recursively call the function for all the adjacent dots
      this.selectDots(i, j-1, frame);
      this.selectDots(i, j+1, frame);
      this.selectDots(i-1, j, frame);
      this.selectDots(i+1, j, frame);			
    }
  }

  // Kill all dots that are 'selected'
  removeSelectedDots() {
    // Go through all the dots
    for (let i = 0; i < this.gridSize; i++) {
      for (let j = 0; j < this.gridSize; j++) {
        let dot = this.getDot(i, j);
        if (dot.selected) {
          // If the dot is selected, kill it with a tween
          this.tweens.add({
            targets: dot, 
            scale: 0,
            duration: 200, 
            onComplete: () => dot.destroy(),
          });
        }
      }
    }
  }

  // Refill the world with dots
  refillDots() {
    this.moveDotsDown();
    this.addMissingDots();

    this.dotsSelected = 0;	
  }

  // Move the dots down to fill the empty dots
  moveDotsDown() {
    // Go through the grid
    for (let i = 0; i < this.gridSize; i++) {
      let moveBy = 0;

      for (let j = this.gridSize-1; j >= 0; j--) {
        let dot = this.getDot(i, j);

        if (!dot) {
          // If a dot is missing
          // It means that the dots above will have to move down
          moveBy += 1;
        } else if (moveBy > 0) {

          // If there is a dot, and it should move down
          // Move it down by the correct amount (moveBy)
          dot.j += moveBy;
          this.tweens.add({
            targets: dot, 
            y: dot.y + moveBy * 50,
            duration: 200, 
          });
        }
      }
    }	
  }

  // Add missing dots 
  addMissingDots() {
    // Go through the grid
    for (let i = 0; i < this.gridSize; i++) {
      for (let j = this.gridSize-1; j >= 0; j--) {
        if (!this.getDot(i, j)) {
        	// If a dot is missing, add a new one
        	this.addDot(i, j);
        }
      }
    }			
  }

  updateScore() {
    // Update score with sound
    this.score += this.dotsSelected * this.dotsSelected;
    this.scoreLabel.setText('score: ' + this.score);
    this.clickSound.play();
    this.tweens.add({
      targets: this.scoreLabel, 
      scale: 1.3,
      duration: 150, 
      yoyo: true,
    });

    // Update move count
    this.moveCount -= 1;
    this.moveLabel.setText('moves: ' + this.moveCount);
    this.tweens.add({
      targets: this.moveLabel, 
      scale: 1.3,
      duration: 150, 
      yoyo: true,
    });

    // If no more moves, end the game
    if (this.moveCount <= 0) {
      this.time.addEvent({
        delay: 600,  
        callback: () => this.scene.start('menu', { score: this.score }),
      });
    }
  }

  // Return the dot i, j
  getDot(i, j) {
    // Get all dots
    let dots = this.dots.getChildren();

    // Find the dot we are looking for
    dots = dots.filter(dot => dot.i === i && dot.j === j);

    // Return the dot, if we found one
    return dots.length === 1 ? dots[0] : null;
  }
}
