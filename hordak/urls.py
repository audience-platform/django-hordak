from django.urls import re_path, include

from hordak.views import accounts, statement_csv_import
from hordak.views import transactions

app_name = "hordak"

urlpatterns = [
    re_path(
        r"^transactions/create/$",
        transactions.TransactionCreateView.as_view(),
        name="transactions_create",
    ),
    re_path(
        r"^transactions/(?P<uuid>.+)/delete/$",
        transactions.TransactionDeleteView.as_view(),
        name="transactions_delete",
    ),
    re_path(
        r"^transactions/currency/$", transactions.CurrencyTradeView.as_view(), name="currency_trade"
    ),
    re_path(
        r"^transactions/reconcile/$",
        transactions.TransactionsReconcileView.as_view(),
        name="transactions_reconcile",
    ),
    re_path(
        r"^transactions/list/$",
        transactions.TransactionsListView.as_view(),
        name="transactions_list",
    ),
    re_path(r"^transactions/legs/$", transactions.LegsListView.as_view(), name="legs_list"),
    re_path(
        r"^statement-line/(?P<uuid>.+)/unreconcile/$",
        transactions.UnreconcileView.as_view(),
        name="transactions_unreconcile",
    ),
    re_path(r"^$", accounts.AccountListView.as_view(), name="accounts_list"),
    re_path(r"^accounts/create/$", accounts.AccountCreateView.as_view(), name="accounts_create"),
    re_path(
        r"^accounts/update/(?P<uuid>.+)/$",
        accounts.AccountUpdateView.as_view(),
        name="accounts_update",
    ),
    re_path(
        r"^accounts/(?P<uuid>.+)/$",
        accounts.AccountTransactionsView.as_view(),
        name="accounts_transactions",
    ),
    re_path(r"^import/$", statement_csv_import.CreateImportView.as_view(), name="import_create"),
    re_path(
        r"^import/(?P<uuid>.*)/setup/$",
        statement_csv_import.SetupImportView.as_view(),
        name="import_setup",
    ),
    re_path(
        r"^import/(?P<uuid>.*)/dry-run/$",
        statement_csv_import.DryRunImportView.as_view(),
        name="import_dry_run",
    ),
    re_path(
        r"^import/(?P<uuid>.*)/run/$",
        statement_csv_import.ExecuteImportView.as_view(),
        name="import_execute",
    ),
]

# Also add in the authentication views that we need to login/logout etc
urlpatterns += [re_path(r"^auth/", include("django.contrib.auth.urls"))]
