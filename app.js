const express = require('express')
const path = require('path')
const { json } = require('express')
const app = express()

//Python connection modules
const spawn = require("child_process").spawn;

debug = true;

// const mul = 2;
// const pythonProcess = spawn('python',["./model/test.py", mul]);
// pythonProcess.stdout.on('data', (data) => {
//   console.log("Data from py script", data.toString());
// });

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


// Values after calculating by backend logic
let CVALUE = {}

app.use(express.json())

// GET
app.get('/api/contacts', (req, res) => {
  debug && console.log('GET request recieved')
  res.status(200).json(SVALUE)
})

// POST
app.post('/api/contacts', (req, res) => {
  debug && console.log('POST request recieved')
  let val = {...req.body}
  SVALUE = val
  console.log(SVALUE)

  async function handleValues(SVALUE) {
    result = await function pythonCall(SVALUE) {
      console.log('Sending data: ', SVALUE)
      const pythonProcess = spawn('python',["./model/main.py", JSON.stringify(SVALUE)]);
      pythonProcess.stdout.on('data', (data) => {
        resValue = data.toString()
        console.log("Data from py script", resValue);
        res.status(200).json(resValue);
      });
    }(val)
    
    


  }

  handleValues()

})


app.use(express.static(path.resolve(__dirname, 'client')))

app.get('*', (req, res) => {
  res.sendFile(path.resolve(__dirname, '@/client', 'index.html'))
})

app.listen(3000, () => console.log('Server has been started on port 3000'))
