# Spotify Canvas Downloader
Tool to get Canvas cover videos from Spotify tracks.

**Note**: As of late 2024, Spotify has updated their authentication system. This now requires a valid `sp_dc` cookie from your browser session.

## ✨ [Try it out](https://canvastify.delitefully.com)

## 🔐 Authentication Setup

Due to Spotify's updated authentication system, you'll need to provide your `sp_dc` cookie:

1. **Get your sp_dc cookie:**
   - Go to [open.spotify.com](https://open.spotify.com) in your browser
   - Log in to your Spotify account
   - Open Developer Tools (F12)
   - Go to Application/Storage → Cookies → https://open.spotify.com
   - Find the `sp_dc` cookie and copy its value

2. **Set the cookie:**
   - Add `SP_DC=your_cookie_value` to your `.env` file, or
   - Set it as an environment variable: `export SP_DC=your_cookie_value`


### Building

- Clone the repository
  ```sh
  git clone https://github.com/Delitefully/spotify-canvas-downloader
  ```
- Configure the env variables
  ```sh
  mv env.example .env
  # Add your SP_DC cookie to the .env file
  ```
- Build the image using Docker Compose
  ```sh
  docker-compose up
  ```

### Development 
Recompile protocol buffer proto (useful when upgrading protobuff): 
```
protoc ./protos/canvas.proto  --python_out=./src/
```
Requires the [Protocol Buffers package](https://developers.google.com/protocol-buffers/docs/downloads).

### API

```http
GET /api/canvas/:trackId
```
Returns 
```json
{
    "success": boolean
    "canvas_url": string, if success is 'true'
    "message": string, error message if success is 'false'
}
```

## ⚠️ Important Notes

- This tool is for educational purposes. Please respect Spotify's Terms of Service.
