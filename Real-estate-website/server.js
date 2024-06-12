const express = require("express");
const { getDb, connectToDb } = require("./db");
const { ObjectId } = require("mongodb");
const diacritics = require("diacritics").remove;

// Initialize app & middleware
const app = express();
app.use(express.json());

const PORT = process.env.PORT || 5000;
let db;

// Sample data for /api/list endpoint
const teamdata = [
  {
    id: 1,
    cover: "../images/list/p-1.png",
    name: "Red Carpet Real Estate",
    location: "Gia bo",
    category: "Authorized",
    price: "$3,700",
    type: "15/11/2022",
  },
  // ... (rest of the data)
];

// Middleware to set CORS headers
app.use((req, res, next) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  next();
});

// Connect to database and start the server
connectToDb((err) => {
  if (!err) {
    app.listen(PORT, () => {
      console.log(`App listening on port ${PORT}`);
    });
    db = getDb();
  }
});

// Root route
app.get("/", (req, res) => {
  res.send("Hello World");
});

// Get document by ID
app.get("/moreinfo/:id", (req, res) => {
  if (ObjectId.isValid(req.params.id)) {
    db.collection("student")
      .findOne({ _id: new ObjectId(req.params.id) })
      .then((doc) => res.status(200).json(doc))
      .catch((err) =>
        res.status(500).json({ error: "Could not fetch the document" })
      );
  } else {
    res.status(500).json({ error: "Invalid ID" });
  }
});

// Get team data
app.get("/api/list", (req, res) => {
  res.send(teamdata);
});

// Pagination for locations
app.get("/location", (req, res) => {
  const page = parseInt(req.query.p) || 0;
  const booksPerPage = 9;
  const books = [];

  db.collection("student")
    .find()
    .sort({})
    .skip(page * booksPerPage)
    .limit(booksPerPage)
    .forEach((book) => books.push(book))
    .then(() => res.status(200).json(books))
    .catch(() =>
      res.status(500).json({ error: "Could not fetch the documents" })
    );
});

// Get locations by city
app.get("/location/:city", (req, res) => {
  const appr = 9;
  const cityMapping = {
    hochiminh: "Hồ Chí Minh",
    hanoi: "Hà Nội",
    binhduong: "Bình Dương",
    quangninh: "Quảng Ninh",
    vungtau: "Vũng Tàu",
  };

  const new_province = cityMapping[req.params.city];
  if (!new_province) {
    return res.status(400).json({ error: "Invalid city parameter" });
  }

  db.collection("student")
    .find({ province: new_province })
    .limit(appr)
    .toArray()
    .then((docs) => res.status(200).json(docs))
    .catch((error) =>
      res.status(500).json({ error: "Could not fetch the documents" })
    );
});

// Get distinct provinces
app.get("/searchcity", (req, res) => {
  db.collection("student")
    .distinct("province")
    .then((docs) => res.status(200).json(docs))
    .catch((error) =>
      res.status(500).json({ error: "Could not fetch the documents" })
    );
});

// Get districts by normalized city name
app.get("/searchdistrict/:city", (req, res) => {
  let city = req.params.city;

  db.collection("student")
    .distinct("province")
    .then((arr) => {
      const matchedCity =
        arr.find((a) => normalizeProvince(a) === city) || "Hồ Chí Minh";

      db.collection("student")
        .distinct("district", { province: matchedCity })
        .then((docs) => res.status(200).json(docs))
        .catch((error) =>
          res.status(500).json({ error: "Could not fetch the documents" })
        );
    })
    .catch((error) =>
      res.status(500).json({ error: "Could not fetch the provinces" })
    );
});

// Utility function to normalize province names
function normalizeProvince(province) {
  if (!province) return "";
  return province
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/\s+/g, "")
    .toLowerCase();
}

// Example route
app.get("/a", (req, res) => {
  res.json({ msg: "Hello world!!!" });
});
