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

app.post('/imagen', upload.single('Incertidumbre.xlsx') , function(req, res) {
    const pythonProcess = spawn("python", ["Incertidumbre.py"])

    pythonProcess.stdout.on('end', function() {
        let image1FileBuffer = fs.readFileSync('uploads/Histograma.png');

        res.send({resizedImage: image1FileBuffer})
    })

    pythonProcess.stdin.end()
})

const PORT = process.env.PORT || 3000
app.listen(PORT, function() {
    console.log('servidor escuchando en el puerto ', PORT)
})