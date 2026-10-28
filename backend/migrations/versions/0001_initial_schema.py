"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-10-28
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ------------------------------------------------------------------ #
    # drug_categories                                                      #
    # ------------------------------------------------------------------ #
    op.create_table(
        "drug_categories",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
        sa.UniqueConstraint("name", name="uq_drug_categories_name"),
    )

    # ------------------------------------------------------------------ #
    # users                                                                #
    # ------------------------------------------------------------------ #
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("nic", sa.String(20), nullable=False),
        sa.Column(
            "user_type",
            sa.Enum(
                "pharmacist",
                "stock_manager",
                "pharmacy_manager",
                "system_administrator",
                name="usertype",
            ),
            nullable=False,
        ),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("contact_number", sa.String(20), nullable=True),
        sa.Column("username", sa.String(100), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("remarks", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("failed_login_attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("locked_until", sa.DateTime(), nullable=True),
        sa.Column("last_login_at", sa.DateTime(), nullable=True),
        sa.Column("created_by_user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
        sa.UniqueConstraint("nic", name="uq_users_nic"),
        sa.UniqueConstraint("username", name="uq_users_username"),
    )

    # ------------------------------------------------------------------ #
    # suppliers                                                            #
    # ------------------------------------------------------------------ #
    op.create_table(
        "suppliers",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("contact_number", sa.String(20), nullable=True),
        sa.Column("special_remarks", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # ------------------------------------------------------------------ #
    # customers                                                            #
    # ------------------------------------------------------------------ #
    op.create_table(
        "customers",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("contact_number", sa.String(20), nullable=False),
        sa.Column("email", sa.String(150), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("dob", sa.Date(), nullable=True),
        sa.Column(
            "gender",
            sa.Enum("male", "female", "other", name="gender"),
            nullable=True,
        ),
        sa.Column("loyalty_points", sa.Numeric(10, 2), nullable=False, server_default="0.00"),
        sa.Column("discount_rate", sa.Numeric(5, 2), nullable=False, server_default="0.00"),
        sa.Column("clinical_remarks", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("ix_customers_contact_number", "customers", ["contact_number"])

    # ------------------------------------------------------------------ #
    # doctors                                                              #
    # ------------------------------------------------------------------ #
    op.create_table(
        "doctors",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("slmc_registration_number", sa.String(50), nullable=False),
        sa.Column("specialization", sa.String(100), nullable=True),
        sa.Column("contact_number", sa.String(20), nullable=True),
        sa.Column("email", sa.String(150), nullable=True),
        sa.Column("hospital", sa.String(200), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
        sa.UniqueConstraint("slmc_registration_number", name="uq_doctors_slmc"),
    )
    op.create_index("ix_doctors_slmc_registration_number", "doctors", ["slmc_registration_number"])

    # ------------------------------------------------------------------ #
    # drugs                                                                #
    # ------------------------------------------------------------------ #
    op.create_table(
        "drugs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("item_code", sa.String(50), nullable=False),
        sa.Column("brand_name", sa.String(200), nullable=False),
        sa.Column("generic_name", sa.String(200), nullable=False),
        sa.Column("active_ingredient", sa.String(200), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("strength", sa.String(50), nullable=True),
        sa.Column(
            "dosage_form",
            sa.Enum("syrup", "tablet", "capsule", "vial", "other", name="dosageform"),
            nullable=False,
        ),
        sa.Column("storage_requirements", sa.String(300), nullable=True),
        sa.Column("batch_number", sa.String(100), nullable=True),
        sa.Column("manufactured_date", sa.Date(), nullable=True),
        sa.Column("expiry_date", sa.Date(), nullable=True),
        sa.Column("unit_price", sa.Numeric(10, 2), nullable=False),
        sa.Column("discount", sa.Numeric(5, 2), nullable=False, server_default="0.00"),
        sa.Column("quantity", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("pack_size", sa.Integer(), nullable=True),
        sa.Column("low_stock_threshold", sa.Integer(), nullable=False, server_default="10"),
        sa.Column("reorder_level", sa.Integer(), nullable=False, server_default="10"),
        sa.Column("is_prescription_only", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("is_otc", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("is_high_alert", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("is_narcotic", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("category_id", sa.Integer(), sa.ForeignKey("drug_categories.id", ondelete="SET NULL"), nullable=True),
        sa.Column("supplier_id", sa.Integer(), sa.ForeignKey("suppliers.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
        sa.UniqueConstraint("item_code", name="uq_drugs_item_code"),
    )
    op.create_index("ix_drugs_item_code", "drugs", ["item_code"])

    # ------------------------------------------------------------------ #
    # prescriptions                                                        #
    # ------------------------------------------------------------------ #
    op.create_table(
        "prescriptions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("customer_id", sa.Integer(), sa.ForeignKey("customers.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("doctor_id", sa.Integer(), sa.ForeignKey("doctors.id", ondelete="SET NULL"), nullable=True),
        sa.Column("issue_date", sa.Date(), nullable=False),
        sa.Column("drug_details_text", sa.Text(), nullable=True),
        sa.Column(
            "reproduce_type",
            sa.Enum("one_time", "recurrent", name="reproducetype"),
            nullable=False,
            server_default="one_time",
        ),
        sa.Column("valid_days", sa.Integer(), nullable=True),
        sa.Column("valid_months", sa.Integer(), nullable=True),
        sa.Column("scan_file_path", sa.String(500), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # ------------------------------------------------------------------ #
    # invoices                                                             #
    # ------------------------------------------------------------------ #
    op.create_table(
        "invoices",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("invoice_number", sa.String(50), nullable=False),
        sa.Column("customer_id", sa.Integer(), sa.ForeignKey("customers.id", ondelete="SET NULL"), nullable=True),
        sa.Column("doctor_id", sa.Integer(), sa.ForeignKey("doctors.id", ondelete="SET NULL"), nullable=True),
        sa.Column("prescription_id", sa.Integer(), sa.ForeignKey("prescriptions.id", ondelete="SET NULL"), nullable=True),
        sa.Column("subtotal", sa.Numeric(12, 2), nullable=False),
        sa.Column("discount_amount", sa.Numeric(12, 2), nullable=False, server_default="0.00"),
        sa.Column("tax_rate", sa.Numeric(5, 2), nullable=False, server_default="0.00"),
        sa.Column("tax_amount", sa.Numeric(12, 2), nullable=False, server_default="0.00"),
        sa.Column("total_amount", sa.Numeric(12, 2), nullable=False),
        sa.Column(
            "payment_mode",
            sa.Enum("cash", "card", "other", name="paymentmode"),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.Enum("completed", "cancelled", name="invoicestatus"),
            nullable=False,
            server_default="completed",
        ),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("cancelled_at", sa.DateTime(), nullable=True),
        sa.Column("cancellation_reason", sa.Text(), nullable=True),
        sa.Column("served_by_user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
        sa.UniqueConstraint("invoice_number", name="uq_invoices_invoice_number"),
    )
    op.create_index("ix_invoices_invoice_number", "invoices", ["invoice_number"])

    # ------------------------------------------------------------------ #
    # invoice_items                                                        #
    # ------------------------------------------------------------------ #
    op.create_table(
        "invoice_items",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("invoice_id", sa.Integer(), sa.ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False),
        sa.Column("drug_id", sa.Integer(), sa.ForeignKey("drugs.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("unit_price", sa.Numeric(10, 2), nullable=False),
        sa.Column("discount_rate", sa.Numeric(5, 2), nullable=False, server_default="0.00"),
        sa.Column("discount_amount", sa.Numeric(10, 2), nullable=False, server_default="0.00"),
        sa.Column("line_total", sa.Numeric(12, 2), nullable=False),
    )

    # ------------------------------------------------------------------ #
    # purchase_orders                                                      #
    # ------------------------------------------------------------------ #
    op.create_table(
        "purchase_orders",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("order_number", sa.String(50), nullable=False),
        sa.Column("supplier_id", sa.Integer(), sa.ForeignKey("suppliers.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("order_date", sa.Date(), nullable=False),
        sa.Column("expected_delivery_date", sa.Date(), nullable=True),
        sa.Column("received_date", sa.Date(), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "draft",
                "submitted",
                "partially_received",
                "received",
                "cancelled",
                name="purchaseorderstatus",
            ),
            nullable=False,
            server_default="draft",
        ),
        sa.Column("remarks", sa.Text(), nullable=True),
        sa.Column("created_by_user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
        sa.UniqueConstraint("order_number", name="uq_purchase_orders_order_number"),
    )
    op.create_index("ix_purchase_orders_order_number", "purchase_orders", ["order_number"])

    # ------------------------------------------------------------------ #
    # purchase_order_items                                                 #
    # ------------------------------------------------------------------ #
    op.create_table(
        "purchase_order_items",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("purchase_order_id", sa.Integer(), sa.ForeignKey("purchase_orders.id", ondelete="CASCADE"), nullable=False),
        sa.Column("drug_id", sa.Integer(), sa.ForeignKey("drugs.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("quantity_ordered", sa.Integer(), nullable=False),
        sa.Column("quantity_received", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("unit_price", sa.Numeric(10, 2), nullable=False),
        sa.Column("line_total", sa.Numeric(12, 2), nullable=False),
        sa.Column("is_free_goods", sa.Boolean(), nullable=False, server_default=sa.false()),
    )

    # ------------------------------------------------------------------ #
    # goods_receipts                                                       #
    # ------------------------------------------------------------------ #
    op.create_table(
        "goods_receipts",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("grn_number", sa.String(50), nullable=False),
        sa.Column("purchase_order_id", sa.Integer(), sa.ForeignKey("purchase_orders.id", ondelete="SET NULL"), nullable=True),
        sa.Column("supplier_id", sa.Integer(), sa.ForeignKey("suppliers.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("received_date", sa.Date(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("received_by_user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
        sa.UniqueConstraint("grn_number", name="uq_goods_receipts_grn_number"),
    )
    op.create_index("ix_goods_receipts_grn_number", "goods_receipts", ["grn_number"])

    # ------------------------------------------------------------------ #
    # goods_receipt_items                                                  #
    # ------------------------------------------------------------------ #
    op.create_table(
        "goods_receipt_items",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("goods_receipt_id", sa.Integer(), sa.ForeignKey("goods_receipts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("drug_id", sa.Integer(), sa.ForeignKey("drugs.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("quantity_received", sa.Integer(), nullable=False),
        sa.Column("unit_cost", sa.Numeric(10, 2), nullable=False),
        sa.Column("is_free_goods", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("batch_number", sa.String(100), nullable=True),
        sa.Column("expiry_date", sa.Date(), nullable=True),
    )

    # ------------------------------------------------------------------ #
    # stock_movements                                                      #
    # ------------------------------------------------------------------ #
    op.create_table(
        "stock_movements",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("drug_id", sa.Integer(), sa.ForeignKey("drugs.id", ondelete="RESTRICT"), nullable=False),
        sa.Column(
            "movement_type",
            sa.Enum(
                "purchase",
                "sale",
                "adjustment",
                "return_to_supplier",
                "transfer_in",
                "transfer_out",
                name="movementtype",
            ),
            nullable=False,
        ),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("unit_cost", sa.Numeric(10, 2), nullable=True),
        sa.Column(
            "reference_type",
            sa.Enum(
                "invoice",
                "purchase_order",
                "goods_receipt",
                "supplier_return",
                "manual",
                name="referencetype",
            ),
            nullable=False,
        ),
        sa.Column("reference_id", sa.Integer(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("performed_by_user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("ix_stock_movements_drug_id", "stock_movements", ["drug_id"])
    op.create_index("ix_stock_movements_created_at", "stock_movements", ["created_at"])

    # ------------------------------------------------------------------ #
    # supplier_returns                                                     #
    # ------------------------------------------------------------------ #
    op.create_table(
        "supplier_returns",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("return_number", sa.String(50), nullable=False),
        sa.Column("supplier_id", sa.Integer(), sa.ForeignKey("suppliers.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("return_date", sa.Date(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("processed_by_user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
        sa.UniqueConstraint("return_number", name="uq_supplier_returns_return_number"),
    )
    op.create_index("ix_supplier_returns_return_number", "supplier_returns", ["return_number"])

    # ------------------------------------------------------------------ #
    # supplier_return_items                                                #
    # ------------------------------------------------------------------ #
    op.create_table(
        "supplier_return_items",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("supplier_return_id", sa.Integer(), sa.ForeignKey("supplier_returns.id", ondelete="CASCADE"), nullable=False),
        sa.Column("drug_id", sa.Integer(), sa.ForeignKey("drugs.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("unit_cost", sa.Numeric(10, 2), nullable=False),
    )

    # ------------------------------------------------------------------ #
    # price_adjustments                                                    #
    # ------------------------------------------------------------------ #
    op.create_table(
        "price_adjustments",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("drug_id", sa.Integer(), sa.ForeignKey("drugs.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("old_price", sa.Numeric(10, 2), nullable=False),
        sa.Column("new_price", sa.Numeric(10, 2), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("adjusted_by_user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("ix_price_adjustments_drug_id", "price_adjustments", ["drug_id"])

    # ------------------------------------------------------------------ #
    # audit_logs                                                           #
    # ------------------------------------------------------------------ #
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("action", sa.String(50), nullable=False),
        sa.Column("entity_type", sa.String(50), nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=True),
        sa.Column("old_value", JSONB, nullable=True),
        sa.Column("new_value", JSONB, nullable=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("ix_audit_logs_user_id", "audit_logs", ["user_id"])
    op.create_index("ix_audit_logs_action", "audit_logs", ["action"])
    op.create_index("ix_audit_logs_entity_type", "audit_logs", ["entity_type"])
    op.create_index("ix_audit_logs_created_at", "audit_logs", ["created_at"])


def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_table("price_adjustments")
    op.drop_table("supplier_return_items")
    op.drop_table("supplier_returns")
    op.drop_table("stock_movements")
    op.drop_table("goods_receipt_items")
    op.drop_table("goods_receipts")
    op.drop_table("purchase_order_items")
    op.drop_table("purchase_orders")
    op.drop_table("invoice_items")
    op.drop_table("invoices")
    op.drop_table("prescriptions")
    op.drop_table("drugs")
    op.drop_table("doctors")
    op.drop_table("customers")
    op.drop_table("suppliers")
    op.drop_table("users")
    op.drop_table("drug_categories")

    op.execute("DROP TYPE IF EXISTS usertype")
    op.execute("DROP TYPE IF EXISTS gender")
    op.execute("DROP TYPE IF EXISTS dosageform")
    op.execute("DROP TYPE IF EXISTS reproducetype")
    op.execute("DROP TYPE IF EXISTS paymentmode")
    op.execute("DROP TYPE IF EXISTS invoicestatus")
    op.execute("DROP TYPE IF EXISTS purchaseorderstatus")
    op.execute("DROP TYPE IF EXISTS movementtype")
    op.execute("DROP TYPE IF EXISTS referencetype")
