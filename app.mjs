import dotenv from 'dotenv';
dotenv.config();
import SpotifyWebApi from 'spotify-web-api-node';
import fs from 'fs';
import util from 'util';
import fetch from 'node-fetch';
const readFile = util.promisify(fs.readFile);

// get api key and client secret from spotify
const spotify_client_id = process.env.SPOTIFY_CLIENT_ID;
const spotify_client_secret = process.env.SPOTIFY_CLIENT_SECRET;

// set up instance of spotify web api node module with my info
const spotifyModule = new SpotifyWebApi({
    clientId: spotify_client_id,
    clientSecret: spotify_client_secret
});

// get token
const getToken = async () => {

    const auth = Buffer.from(spotify_client_id + ':' + spotify_client_secret).toString('base64');

    const result = await fetch('https://accounts.spotify.com/api/token', {
        method: 'POST',
        headers: {
            'Content-Type' : 'application/x-www-form-urlencoded',
            'Authorization' : 'Basic ' + auth
        },
        body: 'grant_type=client_credentials'
    });

    const data = await result.json();
    return data.access_token;
}

//getToken().then(token => console.log(token)).catch(err => console.error(err));

console.log("I got here");

// from an album id, get relevant info and return
const getAlbumDetails = async(albumId) => {
    const info = await spotifyModule.getAlbum(albumId);
    const album_name = info.body.name;
    const artists = info.body.artists.map(artist => artist.name).join(", ");
    const release_date = info.body.release_date;
    return { album_name, artists, release_date }
}

// read all info from album file
async function readAlbumFile() {
    return readFile('albumlist.txt', 'utf8')
}

// create album object with necessary info
async function makeAlbumInfoObject() {
    // empty dictionary-like object to store album info
    const album_info_kvp = {}

    const aToken = await getToken();
    spotifyModule.setAccessToken(aToken);

    // get object of contents of albumlist.txt file
    const album_id_list = await readAlbumFile();

    // put that in new array object where each id is its own element
    const album_id_array = album_id_list.split('\n');

    // make dictionary-like object where ids are keys and value is null
    for (const current_id of album_id_array) {
        const albumDetails = await getAlbumDetails(current_id)
        album_info_kvp[current_id] = albumDetails;
    }

    return album_info_kvp
}

// main
async function main() {
    const album_info_object = await makeAlbumInfoObject();
    console.log(album_info_object);

}

main().catch(console.error);
 







