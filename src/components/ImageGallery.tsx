import React from 'react'
import { ImageData } from '../data/images'

interface ImageGalleryProps {
  images: ImageData[]
  title?: string
  columns?: 1 | 2 | 3 | 4
  showDescription?: boolean
  showTags?: boolean
  onImageClick?: (image: ImageData) => void
}

const ImageGallery: React.FC<ImageGalleryProps> = ({
  images,
  title,
  columns = 3,
  showDescription = false,
  showTags = false,
  onImageClick
}) => {
  const getGridClass = () => {
    switch (columns) {
      case 1: return 'grid-cols-1'
      case 2: return 'grid-cols-1 md:grid-cols-2'
      case 3: return 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3'
      case 4: return 'grid-cols-1 md:grid-cols-2 lg:grid-cols-4'
      default: return 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3'
    }
  }

  return (
    <div className="mb-8">
      {title && (
        <h3 className="text-xl font-semibold text-morocco-red mb-4">
          {title}
        </h3>
      )}
      <div className={`grid ${getGridClass()} gap-4`}>
        {images.map((image) => (
          <div 
            key={image.id} 
            className={`relative group ${onImageClick ? 'cursor-pointer' : ''}`}
            onClick={() => onImageClick?.(image)}
          >
            <img 
              src={image.url} 
              alt={image.alt}
              className="w-full h-48 object-cover rounded-lg transition-transform group-hover:scale-105"
              loading="lazy"
            />
            <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-40 transition-all rounded-lg flex items-center justify-center">
              <div className="text-white text-center opacity-0 group-hover:opacity-100 transition-opacity p-4">
                <span className="font-medium block">{image.location || image.alt}</span>
                {showTags && image.tags.length > 0 && (
                  <div className="mt-2 flex flex-wrap justify-center gap-1">
                    {image.tags.slice(0, 3).map((tag, index) => (
                      <span 
                        key={index}
                        className="bg-morocco-gold bg-opacity-80 text-xs px-2 py-1 rounded-full"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>
            {showDescription && image.description && (
              <div className="mt-2 p-2 bg-gray-50 rounded">
                <p className="text-sm text-gray-700">{image.description}</p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default ImageGallery