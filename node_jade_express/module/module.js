var mongoose = require('mongoose')

var MovieSchema = new mongoose.Schema({
	doctor: String,
	title: String,
	language: String,
	country: String,
	meta: {
		createAt: {
			type: Date,
			defualt: Date.now()
		}
	}
})