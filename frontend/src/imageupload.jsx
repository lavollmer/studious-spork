// src/ImageUpload.js
import React, { useState } from "react";

const ImageUpload = () => {
  const [image, setImage] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(URL.createObjectURL(file));
    }
  };

  const handleImageUpload = async () => {
    if (!image) return;

    setIsLoading(true);
    const formData = new FormData();
    formData.append("file", image);

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        setProcessedImage(url);
      } else {
        alert("Failed to process the image");
      }
    } catch (error) {
      console.error("Error uploading image:", error);
      alert("Error uploading image");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <div className="space-y-4">
        <input
          type="file"
          accept="image/*"
          onChange={handleImageChange}
          className="block mx-auto border p-2"
        />
        <button
          onClick={handleImageUpload}
          disabled={isLoading}
          className="block mx-auto px-4 py-2 bg-blue-500 text-white rounded-md"
        >
          {isLoading ? "Processing..." : "Upload and Process Image"}
        </button>

        {processedImage && (
          <div className="mt-4">
            <img src={processedImage} alt="Processed Artwork" className="max-w-full h-auto" />
          </div>
        )}
      </div>
    </div>
  );
};

export default ImageUpload;
