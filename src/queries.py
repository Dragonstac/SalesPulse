from database import run_query 
class SalesAnalytics:
    @staticmethod
    def get_kpis(region=None):
        where = "WHERE r.region_name = %(region)s" if region and region != "All Regions" else ""
        sql = f"""
            SELECT 
                SUM(o.total_amount) as revenue,
                COUNT(DISTINCT o.order_id) as orders,
                COUNT(DISTINCT c.customer_id) as active_customers
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            JOIN regions r ON c.region_id = r.region_id
            {where}
        """
        return run_query(sql, {'region': region})

    @staticmethod
    def get_trend(region=None):
        where = "WHERE r.region_name = %(region)s" if region and region != "All Regions" else ""
        sql = f"""
            SELECT DATE_TRUNC('month', o.order_date) as month, SUM(o.total_amount) as revenue
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            JOIN regions r ON c.region_id = r.region_id
            {where}
            GROUP BY 1 ORDER BY 1
        """
        return run_query(sql, {'region': region})

    @staticmethod
    def get_top_products(region=None):
        where = "WHERE r.region_name = %(region)s" if region and region != "All Regions" else ""
        sql = f"""
            SELECT p.product_name, SUM(oi.quantity * oi.unit_price) as revenue
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.order_id
            JOIN products p ON oi.product_id = p.product_id
            JOIN customers c ON o.customer_id = c.customer_id
            JOIN regions r ON c.region_id = r.region_id
            {where}
            GROUP BY 1 ORDER BY 2 DESC LIMIT 5
        """
        return run_query(sql, {'region': region})