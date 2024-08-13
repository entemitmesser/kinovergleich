<?php
header('Content-Type: application/json');
$database = 'path_to_your_sqlite_database.db';

try {
    $conn = new PDO("sqlite:" . $database);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $stmt = $conn->query("SELECT title, playtime_price, 'undefined' as duration, location, url FROM movies");
    $movies = [];
    while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
        $row['location'] = ['name' => $row['location'], 'url' => $row['url']];
        unset($row['url']);
        $movies[] = $row;
    }

    echo json_encode($movies);
} catch (PDOException $e) {
    echo json_encode(['error' => $e->getMessage()]);
}
?>


