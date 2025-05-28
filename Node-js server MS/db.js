const mongoose=require('mongoose');
const mongoURI="mongodb+srv://rakeshyana976:Dhangar976@cluster0.af0wm.mongodb.net/"

const connectToMongo=()=>{
    mongoose.connect(mongoURI,()=>{
        console.log("connected to mongo successfully");
    })
}
module.exports=connectToMongo;