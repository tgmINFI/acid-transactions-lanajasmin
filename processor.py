import sqlite3

class ShipmentProcessor:
    def __init__(self, db_path):
        self.db_path = db_path

    def process_shipment(self, item_name, quantity, log_callback):
        """
        Executes the shipment logic.
        :param item_name: Name of the item
        :param quantity: Amount to move
        :param log_callback: A function to print to the GUI console
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        log_callback(f"--- STARTING TRANSACTION: Move {quantity} of {item_name} ---")

        # ==============================================================================
        # STUDENT TODO: Fix the Transaction Logic below.
        # Currently, if Step 1 fails, Step 2 still runs, creating a "Ghost Shipment".
        # Ensure the operation is ATOMIC (All or Nothing).
        # ==============================================================================

        try:
        # STEP 1: Update Inventory
            cursor.execute("UPDATE inventory SET stock_qty = stock_qty - ? WHERE item_name = ?", 
                           (quantity, item_name))
            log_callback(">> STEP 1 SUCCESS: Inventory Deducted.")

        # STEP 2: Log the Shipment
            cursor.execute("INSERT INTO shipment_log (item_name, qty_moved) VALUES (?, ?)", 
                           (item_name, quantity))
            log_callback(">> STEP 2 SUCCESS: Shipment Logged.")

        # Wenn wir hier ankommen, war alles erfolgreich
            conn.commit()
            log_callback("--- TRANSACTION COMMITTED SUCCESSFULLY ---")

        except Exception as e:
            # Wenn IRGENDEIN Fehler auftritt, machen wir alles rückgängig
            conn.rollback()
            log_callback(f"!! TRANSACTION FAILED: {e}. Rollback executed !!")
        
        finally:
            # Verbindung immer schließen, egal ob Erfolg oder Fehler
            conn.close()
        
        conn.close()