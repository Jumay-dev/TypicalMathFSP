const express = require('express')
const path = require('path')
const { json } = require('express')
let app = express()
var cors = require('cors')


// app.use(cors())

// app.options('*', cors())

app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*')
  res.header('Access-Control-Allow-Headers', '*')
  if (req.method === 'OPTIONS') {
    res.header('Access-Control-Allow-Methods', 'PUT, POST, PATCH, DELETE, GET')
    return res.status(200).json({ })
  }
  next()
})

let tasks

const {MongoClient} = require('mongodb')

async function main(){
  const uri = "mongodb+srv://type_user:345125@cluster0.znmke.mongodb.net/<dbname>?retryWrites=true&w=majority"
  const client = new MongoClient(uri);
  try {
      // Connect to the MongoDB cluster
      await client.connect();
      // get all documents in collection
      tasks = await client.db("typicalmath").collection("taskList").find({}).toArray();
  } catch (e) {
      console.error(e);
  } finally {
      await client.close();
  }
}

main().catch(console.error);

//Python connection modules
const spawn = require("child_process").spawn;

debug = true;


// Start values for example
let SVALUE = {
  vx: 0.593397,
  vy: 5.793711,
  vz: 4.948645,
  x: 4226.800251,
  y: 3085.944251,
  z: -4321.376266,
  tstart: 0,
  dt: 0.1,
  tend: 100
}

app.use(express.json())

// GET's
app.get('/api/tasks', (req, res) => {
  let timeNow = currentTime()
  debug && console.log('GET tasks in ', timeNow)
  main().catch(console.error)
  // res.setHeader('Access-Control-Allow-Origin', '*');
  // res.setHeader('Access-Control-Allow-Methods', '*');
  // res.setHeader('Access-Control-Allow-Headers', 'origin, content-type, accept');
  res.status(200).json(tasks)
})

app.get('/api/fields', (req, res) => {
  let timeNow = currentTime()
  let IP = req.connection.remoteAddress;
  debug && console.log('GET fields in ', timeNow, ' from: ', IP)
  main().catch(console.error);
  res.status(200).json(tasks[0].fields)
})

// POST's
app.post('/api/contacts', (req, res) => {
  let timeNow = currentTime()
  debug && console.log('POST calc req: ', timeNow)
  let val = {...req.body}
  SVALUE = val

  async function handleValues(SVALUE) {
    result = function pythonCall(SVALUE) {
      const pythonProcess = spawn('python',["./model/main.py", JSON.stringify(SVALUE)]);
      pythonProcess.stdout.on('data', (data) => {
        // let resValue = JSON.parse(data);
        // res.status(200).json(data);
        // debug && console.log(data.toString());
        return res.send(JSON.stringify(data.toString()));
      });
    }(val)
  }
  handleValues()
})

function currentTime() {
  Data = new Date();
  Hour = Data.getHours();
  Minutes = Data.getMinutes();
  Seconds = Data.getSeconds();
  return Hour + ':' + Minutes + ':' + Seconds
}


// app.use(express.static(path.resolve(__dirname, 'client')))

// app.get('*', (req, res) => {
//   res.sendFile(path.resolve(__dirname, '@/client', 'index.html'))
// })

app.listen(3000, () => console.log('Server has been started on port 3000'))
