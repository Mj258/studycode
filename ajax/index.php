<?php
	function index(){
		echo "string";
	}
	function create(){
		if(!isset($_POST['name'])&&empty($_POST['name'])){
			echo "string";
		}
	}
?>