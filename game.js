// Set up canvas and context
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// Set canvas size to full screen
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Load images
const characterNormal = new Image();
characterNormal.src = 'danielbaldpants.png';
const characterMouth = new Image();
characterMouth.src = 'danielbaldmouth.png';

const burgerImg = new Image();
burgerImg.src = 'burger.png';
const chickenWingImg = new Image();
chickenWingImg.src = 'ChickenWing.png';
const eggplantImg = new Image();
eggplantImg.src = 'eggplant.png';
const cucumberImg = new Image();
cucumberImg.src = 'cumber.png';
const chipImg = new Image();
chipImg.src = 'chip.png';

const foodImages = [burgerImg, chickenWingImg, eggplantImg, cucumberImg, chipImg];

// Set up character attributes
let characterSize = 200;
let characterX = canvas.width / 2 - characterSize / 2;
let characterY = canvas.height - characterSize - 100;
let characterSpeed = 10;
let currentCharacterImage = characterNormal;

// Set up food attributes
let foodList = [];
let foodSpeed = 5;
let foodSize = 100;
let score = 0;
let gameDuration = 60; // in seconds
let startTime = Date.now();
let foodSpawnTime = 25;
let frames = 0;

// Game loop
function gameLoop() {
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw character
    ctx.drawImage(currentCharacterImage, characterX, characterY, characterSize, characterSize);

    // Handle food falling
    if (frames % foodSpawnTime === 0) {
        const foodX = Math.random() * (canvas.width - foodSize);
        const foodImage = foodImages[Math.floor(Math.random() * foodImages.length)];
        foodList.push({x: foodX, y: -foodSize, image: foodImage});
    }

    let foodNearby = false;
    for (let i = foodList.length - 1; i >= 0; i--) {
        const food = foodList[i];
        food.y += foodSpeed;

        // Draw food
        ctx.drawImage(food.image, food.x, food.y, foodSize, foodSize);

        // Check if food is caught
        if (food.y + foodSize > characterY && food.y < characterY + characterSize &&
            food.x + foodSize > characterX && food.x < characterX + characterSize) {
            foodList.splice(i, 1);
            score += 1;
            foodNearby = true;
        }

        // Remove food that falls off the screen
        if (food.y > canvas.height) {
            foodList.splice(i, 1);
        }

        // Check proximity for mouth image change
        if (food.y + foodSize > characterY && food.x + foodSize > characterX) {
            foodNearby = true;
        }
    }

    // Change character image based on proximity
    currentCharacterImage = foodNearby ? characterMouth : characterNormal;

    // Display score
    ctx.font = "30px Arial";
    ctx.fillStyle = "white";
    ctx.fillText(`Score: ${score}`, 20, 40);

    // Display timer
    let elapsedTime = Math.floor((Date.now() - startTime) / 1000);
    let remainingTime = Math.max(0, gameDuration - elapsedTime);
    ctx.fillText(`Time Left: ${remainingTime}s`, 20, 80);

    // Check game over condition
    if (remainingTime <= 0) {
        ctx.fillText("Game Over!", canvas.width / 2 - 100, canvas.height / 2);
        return; // Stop the game loop
    }

    frames++;
    requestAnimationFrame(gameLoop);
}

// Start the game loop
gameLoop();

// Handle character movement with arrow keys
window.addEventListener("keydown", (event) => {
    switch(event.key) {
        case "ArrowLeft":
            characterX = Math.max(0, characterX - characterSpeed);
            break;
        case "ArrowRight":
            characterX = Math.min(canvas.width - characterSize, characterX + characterSpeed);
            break;
    }
});
