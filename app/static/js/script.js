document.addEventListener("DOMContentLoaded", () => {
    const stickers = document.querySelectorAll(".sticker");
    const container = document.getElementById("sticker-container");
  
    // Container dimensions
    const containerWidth = container.offsetWidth;
    const containerHeight = container.offsetHeight;
  
    // Maximum and minimum sticker size
    const maxStickerSize = 400;
    const minStickerSize = 200;
  
    // Number of stickers and their size decrement
    const numStickers = stickers.length;
    const sizeDecrement = (maxStickerSize - minStickerSize) / numStickers;
  
    const centerX = containerWidth / 2; // Center X position
    const centerY = containerHeight / 2; // Center Y position
    const baseDistance = 250; // Base distance from the main sticker
  
    stickers.forEach((sticker, index) => {
      // Dynamically calculate the size for the current sticker
      const stickerSize = maxStickerSize - sizeDecrement * index;
  
      let top, left;
  
      if (index === 0) {
        // Center the first sticker
        top = centerY - stickerSize / 2;
        left = centerX - stickerSize / 2;
      } else {
        // Divide the circle evenly
        const angle = (2 * Math.PI * index) / numStickers; // Calculate angle for this sticker
  
        // Calculate distance with slight randomness for a natural look
        const distance = baseDistance + Math.random() * 60;
  
        // Convert polar coordinates (angle and distance) to Cartesian coordinates (x, y)
        top = centerY + Math.sin(angle) * distance - stickerSize / 2 +100;
        left = centerX + Math.cos(angle) * distance*2 - stickerSize / 2  + 100;
      }
  
      // Apply styles
      const rotation = Math.random() * 30 - 15; // Random rotation between -15 and 15 degrees
      const zIndex = numStickers - index; // Ensure main sticker is on top
  
      sticker.style.position = "absolute";
      sticker.style.width = `${stickerSize}px`;
      sticker.style.height = "auto";
      sticker.style.top = `${top}px`;
      sticker.style.left = `${left}px`;
      sticker.style.transform = `rotate(${rotation}deg)`;
      sticker.style.zIndex = zIndex;
    });
  });
  