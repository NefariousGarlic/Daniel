// Set up canvas and context
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// Set canvas size to full screen
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Load images with onload callbacks to ensure they are drawn after loading
const characterNormal = new Image();
const characterMouth = new Image();
const burgerImg = new Image();
const chickenWingImg = new Image();
const eggplantImg = new Image();
const cucumberImg = new Image();
const chipImg = new Image();

let imagesLoaded = 0;
const totalImages = 7; // Number of images to load

characterNormal.src = 'danielbaldpants.png';
characterMouth.src = 'danielbaldmouth.png';
burgerImg.src = 'burger.png';
chickenWingImg.src = 'ChickenWing.png';
eggplantImg.src = 'eggplant.png';
cucumberImg.src = 'cumber.png';
chipImg.src = 'chip.png';

// List of food images
const foodImages = [burgerImg, chickenWingImg, eggplantImg, cucumberImg, chipImg];

// Load images and ensure the game starts when all images are loaded
function imageLoaded() {
    imagesLoaded++;
    if (imagesLoaded === totalImages) {
        // Start the game loop once all images are loaded
        gameLoop();
    }
}

// Attach load event listeners to ensure images are fully loaded
characterNormal.onload = imageLoaded;
characterMouth.onload = imageLoaded;
burgerImg.onload = imageLoaded;
chickenWingImg.onload = imageLoaded;
eggplantImg.onload = imageLoaded;
cucumberImg.onload = imageLoaded;
chipImg.onload = imageLoaded;

// Set up character attributes
let characterSize = 400;
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
