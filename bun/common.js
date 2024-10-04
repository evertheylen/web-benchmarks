const { Pool } = require("pg");

if (process.env.SERVER_THREADS !== undefined) {
	cpus = parseInt(process.env.SERVER_THREADS);
} else {
	throw new Error('no SERVER_THREADS env var')
}
console.log(`Using ${cpus} threads`);
// 240 = lcm(1 2 4 8 12 16 20)
const poolSize = Math.floor(240 / cpus);

class User {
	constructor(obj) {
		this.id = obj.id;
		this.username = obj.username;
		this.name = obj.name;
		this.sex = obj.sex;
		this.address = obj.address;
		this.mail = obj.mail;
		this.birthdate = obj.birthdate.toISOString();
	}
}

/**
 * @param {string} str
 * @return {string}
 */
function caesarCipher(str) {
	const key = 14;
    const buf = Buffer.allocUnsafe(str.length);
    const maxASCII = 127;

	for (var i = 0; i < str.length; i ++) {
		let newCode = str.charCodeAt(i);

		if (newCode >= 0 && newCode <= maxASCII) {
			newCode += key;

			if (newCode > maxASCII) {
				newCode -= 26;
			} else if (newCode < 0) {
				newCode += 26;
			}
		}

		buf[i] = newCode;
	}

	return buf.toString('ascii');
}


// const db = new Pool({
// 	host: 'localhost',
// 	port: process.env.PG_PORT,
// 	database: process.env.PG_DB,
// 	user: process.env.PG_USER,
// 	password: process.env.PG_PASS,
// 	min: poolSize,
// 	max: poolSize,
// });

async function getUsers() {
	//const result = await db.query('SELECT * FROM "user";');
	const result = [
		{
			id: 1,
			username: 'erica81',
			name: 'Donald Walker',
			sex: 'M',
			address: '38908 Debra Neck\nNew Lisatown, OH 45098',
			mail: 'jasongallagher@gmail.com',
			birthdate: new Date("1956-01-08T23:00:00.000Z"),
		},
		{
			id: 2,
			username: 'amanda61',
			name: 'Lindsey Roman',
			sex: 'F',
			address: '5931 Jeremy Glens Apt. 316\nNew Michael, GA 35494',
			mail: 'frances19@yahoo.com',
			birthdate: new Date("1977-01-03T23:00:00.000Z"),
		},
		{
			id: 3,
			username: 'angela50',
			name: 'James Mayo',
			sex: 'M',
			address: '41395 Victor Tunnel\nDouglasland, NE 98413',
			mail: 'rachael65@gmail.com',
			birthdate: new Date("1923-02-21T00:00:00.000Z"),
		},
		{
			id: 4,
			username: 'laura69',
			name: 'Anthony Rodriguez',
			sex: 'M',
			address: '848 Smith Roads\nAmandaburgh, CO 57486',
			mail: 'smithjennifer@hotmail.com',
			birthdate: new Date("1972-06-10T23:00:00.000Z"),
		},
		{
			id: 5,
			username: 'kromero',
			name: 'Brian Garrett',
			sex: 'M',
			address: '809 Andrew Viaduct\nDeckerburgh, UT 10823',
			mail: 'tuckerchad@hotmail.com',
			birthdate: new Date("2008-07-16T22:00:00.000Z"),
		},
		{
			id: 6,
			username: 'catherine38',
			name: 'Theresa Martin',
			sex: 'F',
			address: '657 Hayes Forge Apt. 098\nEast Chadstad, VA 43810',
			mail: 'youngelizabeth@gmail.com',
			birthdate: new Date("1922-04-27T23:00:00.000Z"),
		},
		{
			id: 7,
			username: 'richarddavis',
			name: 'Kenneth Sanchez',
			sex: 'M',
			address: '0106 Mcbride Court\nSouth Donaldville, UT 10381',
			mail: 'michellepierce@gmail.com',
			birthdate: new Date("1977-11-19T23:00:00.000Z"),
		},
		{
			id: 8,
			username: 'jasonmorales',
			name: 'Dr. Samuel Martin',
			sex: 'M',
			address: '474 Susan Well\nJenniferland, WI 76415',
			mail: 'bruce50@gmail.com',
			birthdate: new Date("1969-03-15T23:00:00.000Z"),
		},
		{
			id: 9,
			username: 'lopezbrooke',
			name: 'Christopher Yu',
			sex: 'M',
			address: '93990 Barnes Passage\nSarahville, ID 52377',
			mail: 'brewerstephen@hotmail.com',
			birthdate: new Date("1914-03-10T00:00:00.000Z"),
		},
		{
			id: 10,
			username: 'william25',
			name: 'Kristine Garcia',
			sex: 'F',
			address: '2784 Archer Ports Apt. 841\nTaylorland, NV 36198',
			mail: 'jasoncooper@hotmail.com',
			birthdate: new Date("1940-03-28T23:00:00.000Z"),
		}
	]
	

	return result.map((row) => {
		row.address = caesarCipher(row.address);

		return new User(row);
	});
}

exports.cpus = cpus;
exports.getUsers = getUsers;
