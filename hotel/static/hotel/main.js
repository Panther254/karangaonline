// console.log("Hello World!!!")

var updateButtons = document.getElementsByClassName('update-tray')

for (var i = 0; i < updateButtons.length; i++) {
	updateButtons[i].addEventListener('click',function () {
		var productID = this.dataset.food
		var action = this.dataset.action
		console.log('ProductID:', productID, 'Action:', action)

		console.log('USER:', user)
		if (user == 'AnonymousUser') {
			console.log('User is Not Authenticated....')
		}else{
			 updateUserOrder(productID, action);
		}
	})
}

function updateUserOrder(productID, action){ 

	console.log('User is Authenticated. Sending data...')

	var url = '/update_tray/'

	fetch(url, {
		method:'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken' :csrftoken,
		},
		body:JSON.stringify({'productID': productID, 'action': action})
	}) 

	.then((response) => {
		return response.json()
	})

	.then((data) => {
		console.log('data:', data)
		location.reload()
	})


}


