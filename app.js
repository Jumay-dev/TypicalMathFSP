const express = require('express')
const path = require('path')
const { json } = require('express')
const app = express()
var cors = require('cors')


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

app.use(cors({origin: 'http://91.193.177.214:3000'}));

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

// let fields =  [
//     {"id": 0, "val": 4226.800251, "varb": "x", "measure": "km"}, 
//     {"id": 1, "val": 3085.944251, "varb": "y", "measure": "km"}, 
//     {"id": 2, "val": -4321.376266, "varb": "z", "measure": "km"},
//     {"id": 3, "val": 0.593397, "varb": "vx", "measure": "km/sec"},
//     {"id": 4, "val": 5.793711, "varb": "vy", "measure": "km/sec"},
//     {"id": 5, "val": 4.948645, "varb": "vz", "measure": "km/sec"},
//     {"id": 6, "val": 0, "varb": "tstart", "measure": "sec"},
//     {"id": 7, "val": 0.1, "varb": "dt", "measure": "sec"},
//     {"id": 8, "val": 2, "varb": "tend", "measure": "sec"} 
//         ]

// let tasks = [
//   {id: 0, title: "Расчет маневра", subtitle: "Кватернионы", text: "Описание задачи будет реализовано здесь", fields},
//   {"id": 1, "title": "Название задачи", "subtitle": "Тип матаппарата", "text": "Описание задачи будет реализовано здесь"},
//   {id: 2, title: "Название задачи", subtitle: "Тип матаппарата", text: "Описание задачи будет реализовано здесь"},
//   {id: 3, title: "Название задачи", subtitle: "Тип матаппарата", text: "Описание задачи будет реализовано здесь"},
//   {id: 4, title: "Название задачи", subtitle: "Тип матаппарата", text: "Описание задачи будет реализовано здесь"},
//   {id: 5, title: "Название задачи", subtitle: "Тип матаппарата", text: "Описание задачи будет реализовано здесь"},
//   {id: 6, title: "Название задачи", subtitle: "Тип матаппарата", text: "Описание задачи будет реализовано здесь"},
//   {id: 7, title: "Название задачи", subtitle: "Тип матаппарата", text: "Описание задачи будет реализовано здесь"},
// ];


app.use(express.json())

// GET's

app.get('/api/tasks', (req, res) => {
  let timeNow = currentTime()
  debug && console.log('GET tasks in ', timeNow)
  main().catch(console.error)
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
