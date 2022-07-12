const  express  =  require ( 'express' ) 
const  app  =  express ( )

app.get('/',function(req, res) {
    res.send('Esta es la pagina')
})

app.listen(3000)