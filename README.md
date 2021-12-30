# Spotify Canvas Downloader
Tool to get Canvas cover videos from Spotify tracks.


## ✨ [Try it out](https://canvastify.delitefully.com)




### Building

- Clone the repository
  ```sh
  git clone https://github.com/Delitefully/spotify-canvas-downloader
  ```
- Configure the env variables

  Note: a Premium Spotify account is required. This is a [librespot](https://github.com/librespot-org/librespot) limitation.
  ```
  mv env.example .env
  ```
- Build the image using Docker Compose
  ```sh
  docker-compose up
  ```

### API

```
GET /api/canvas/:trackId
```
Returns 
```
{
    success: boolean
    canvas_url: string, if success is 'true'
    message: string, error message if success is 'false'
}
```
