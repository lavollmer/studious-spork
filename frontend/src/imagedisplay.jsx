// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import './App.css'
// src/ImageDisplay.js
import React, { useEffect, useRef } from "react";

const ImageDisplay = () => {
  const imgRef = useRef(null);

  useEffect(() => {
    const handleScreenshotAttempt = () => {
      // This function will be called if a screenshot is attempted
      console.log("Screenshot detected");
      alert("Screenshot detected!");  // You can replace this with more behavior like logging, blocking, etc.
    };

    // Simulating a screenshot detection with the window capture (using visibility change event)
    const onVisibilityChange = () => {
      if (document.hidden) {
        handleScreenshotAttempt();
      }
    };

    document.addEventListener("visibilitychange", onVisibilityChange);

    return () => {
      document.removeEventListener("visibilitychange", onVisibilityChange);
    };
  }, []);

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <div className="relative">
        <img
          ref={imgRef}
          src="/protected_medicinebottle_more_distorted.png"
          alt="Protected Artwork"
          className="max-w-full h-auto"
        />
      </div>
    </div>
  );
};

export default ImageDisplay;
