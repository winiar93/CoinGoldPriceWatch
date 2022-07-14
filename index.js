const express = require('express');
const redis = require('redis');
const process = require('process');

const app = express();
const client = redis.createClient({
    host: 'redis-server',
    port: 6379
});

client.set('visits', 0);

app.get("/", (req, res) => {
    client.get('visits', (err, visits) => {
        res.send('Number of visits: ' + visits);
        client.set('visits', parseInt(visits) + 1);

    });
});

app.listen(8081, () =>{
    console.log("listening on port 8080");
});


// import express from "express";
// import { createClient } from 'redis';
 
// const app = express();
 
// const client = createClient({
//   url: 'redis://default:default@redis-server:6379'
// });
 
// (async () => {
//   client.on('error', (err) => console.log('Redis Client Error', err));
 
//   await client.connect();
//   await client.set('visits', 0);
//   // const value = await client.get('key');
// })();
 
// // client.set('visits', 0);
 
// app.get('/', async (req, res) => {
//   const visits = await client.get('visits')
//   res.send(`Number of visits is ${visits}`);
//   await client.set('visits', parseInt(visits) + 1);
// });
 
// app.listen(8081, () => {
//   console.log('Listening on port 8081');
// });