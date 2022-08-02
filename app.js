const  express  =  require ( 'express' ) 
const multer = require ('multer')
const spawn = require("child_process").spawn
const fs = require ('fs')

const storage = multer.diskStorage({
    destination: function (req, file, cb) {
      cb(null, 'uploads/')
    },
    filename: function (req, file, cb) {
      cb(null, file.fieldname)
    }
})
  
const upload = multer({ storage: storage })
const app = express()
app.use(express.json())

app.get('/', function(req, res) {
    res.send('Hola Mundo!!')
})


app.post('/imagen1', upload.single('Incertidumbre.xlsx') , function(req, res) {
    const pythonProcess = spawn("python", ["Incertidumbre.py"])
    pythonProcess.stdout.on('end', function() {
        let image1FileBuffer = fs.readFileSync('uploads/Histograma.png');
        res.send({'$content-type': 'image/png', '$content': image1FileBuffer.toString('base64')})
    })
    pythonProcess.stdin.end()
})


app.post('/imagen2', upload.single('Incertidumbre.xlsx') , function(req, res) {
  const pythonProcess = spawn("python", ["Incertidumbre.py"])
  pythonProcess.stdout.on('end', function() {
      let image1FileBuffer = fs.readFileSync('uploads/Tornado.png');
      res.send({'$content-type': 'image/png', '$content': image1FileBuffer.toString('base64')})
  })
  pythonProcess.stdin.end()
})


app.post('/imagen3', upload.single('Riesgo.xlsx') , function(req, res) {
  const pythonProcess = spawn("python", ["Riesgo.py"])
  pythonProcess.stdout.on('end', function() {
      let image1FileBuffer = fs.readFileSync('uploads/Histograma2.png');
      res.send({'$content-type': 'image/png', '$content': image1FileBuffer.toString('base64')})
  })
  pythonProcess.stdin.end()
})


app.post('/imagen4', upload.single('Riesgo.xlsx') , function(req, res) {
  const pythonProcess = spawn("python", ["Riesgo.py"])
  pythonProcess.stdout.on('end', function() {
      let image1FileBuffer = fs.readFileSync('uploads/Tornado2.png');
      res.send({'$content-type': 'image/png', '$content': image1FileBuffer.toString('base64')})
  })
  pythonProcess.stdin.end()
})

const PORT = process.env.PORT || 3000
app.listen(PORT, function() {
    console.log('servidor escuchando en el puerto ', PORT)
})