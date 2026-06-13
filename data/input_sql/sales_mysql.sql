CREATE TABLE `sales_records` (
  `sale_id` int(11) NOT NULL AUTO_INCREMENT,
  `product_name` varchar(100) NOT NULL,
  `quantity` int(11) DEFAULT '0',
  `sale_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`sale_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SELECT `product_name`, SUM(`quantity`) AS total_sold
FROM `sales_records`
WHERE `sale_date` >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY `product_name`
ORDER BY total_sold DESC
LIMIT 10;
