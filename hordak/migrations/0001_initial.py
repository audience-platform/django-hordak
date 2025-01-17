# Generated by Django 4.0.1 on 2022-01-13 11:02

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import djmoney.models.fields
import hordak.models.core
import mptt.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='uuid')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('code', models.CharField(blank=True, max_length=3, null=True, verbose_name='code')),
                ('full_code', models.CharField(blank=True, db_index=True, max_length=100, null=True, unique=True, verbose_name='full_code')),
                ('type', models.CharField(blank=True, choices=[('AS', 'Asset'), ('LI', 'Liability'), ('IN', 'Income'), ('EX', 'Expense'), ('EQ', 'Equity'), ('TR', 'Currency Trading')], max_length=2, verbose_name='type')),
                ('is_bank_account', models.BooleanField(blank=True, default=False, help_text='Is this a bank account. This implies we can import bank statements into it and that it only supports a single currency', verbose_name='is bank account')),
                ('currencies', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=3), db_index=True, size=None, verbose_name='currencies')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='hordak.account', verbose_name='parent')),
            ],
            options={
                'verbose_name': 'account',
                'unique_together': {('parent', 'code')},
            },
        ),
        migrations.CreateModel(
            name='StatementImport',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='uuid')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='timestamp')),
                ('source', models.CharField(help_text='A value uniquely identifying where this data came from. Examples: "csv", "teller.io".', max_length=20, verbose_name='source')),
                ('extra', models.JSONField(default=hordak.models.core.json_default, help_text='Any extra data relating to the import, probably specific to the data source.', verbose_name='extra')),
                ('bank_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imports', to='hordak.account', verbose_name='bank account')),
            ],
            options={
                'verbose_name': 'statementImport',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='uuid')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, help_text='The creation date of this transaction object', verbose_name='timestamp')),
                ('date', models.DateField(default=django.utils.timezone.now, help_text='The date on which this transaction occurred', verbose_name='date')),
                ('description', models.TextField(blank=True, default='', verbose_name='description')),
            ],
            options={
                'verbose_name': 'transaction',
                'get_latest_by': 'date',
            },
        ),
        migrations.CreateModel(
            name='TransactionCsvImport',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='uuid')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='timestamp')),
                ('has_headings', models.BooleanField(default=True, verbose_name='First line of file contains headings')),
                ('file', models.FileField(upload_to='transaction_imports', verbose_name='CSV file to import')),
                ('state', models.CharField(choices=[('pending', 'Pending'), ('uploaded', 'Uploaded, ready to import'), ('done', 'Import complete')], default='pending', max_length=20, verbose_name='state')),
                ('date_format', models.CharField(choices=[('%d-%m-%Y', 'dd-mm-yyyy'), ('%d/%m/%Y', 'dd/mm/yyyy'), ('%d.%m.%Y', 'dd.mm.yyyy'), ('%d-%Y-%m', 'dd-yyyy-mm'), ('%d/%Y/%m', 'dd/yyyy/mm'), ('%d.%Y.%m', 'dd.yyyy.mm'), ('%m-%d-%Y', 'mm-dd-yyyy'), ('%m/%d/%Y', 'mm/dd/yyyy'), ('%m.%d.%Y', 'mm.dd.yyyy'), ('%m-%Y-%d', 'mm-yyyy-dd'), ('%m/%Y/%d', 'mm/yyyy/dd'), ('%m.%Y.%d', 'mm.yyyy.dd'), ('%Y-%d-%m', 'yyyy-dd-mm'), ('%Y/%d/%m', 'yyyy/dd/mm'), ('%Y.%d.%m', 'yyyy.dd.mm'), ('%Y-%m-%d', 'yyyy-mm-dd'), ('%Y/%m/%d', 'yyyy/mm/dd'), ('%Y.%m.%d', 'yyyy.mm.dd'), ('%d-%m-%y', 'dd-mm-yy'), ('%d/%m/%y', 'dd/mm/yy'), ('%d.%m.%y', 'dd.mm.yy'), ('%d-%y-%m', 'dd-yy-mm'), ('%d/%y/%m', 'dd/yy/mm'), ('%d.%y.%m', 'dd.yy.mm'), ('%m-%d-%y', 'mm-dd-yy'), ('%m/%d/%y', 'mm/dd/yy'), ('%m.%d.%y', 'mm.dd.yy'), ('%m-%y-%d', 'mm-yy-dd'), ('%m/%y/%d', 'mm/yy/dd'), ('%m.%y.%d', 'mm.yy.dd'), ('%y-%d-%m', 'yy-dd-mm'), ('%y/%d/%m', 'yy/dd/mm'), ('%y.%d.%m', 'yy.dd.mm'), ('%y-%m-%d', 'yy-mm-dd'), ('%y/%m/%d', 'yy/mm/dd'), ('%y.%m.%d', 'yy.mm.dd')], default='%d-%m-%Y', max_length=50, verbose_name='date format')),
                ('hordak_import', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hordak.statementimport', verbose_name='hordak import')),
            ],
        ),
        migrations.CreateModel(
            name='StatementLine',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='uuid')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='timestamp')),
                ('date', models.DateField(verbose_name='date')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=13, verbose_name='amount')),
                ('description', models.TextField(blank=True, default='', verbose_name='description')),
                ('type', models.CharField(default='', max_length=50, verbose_name='type')),
                ('source_data', models.JSONField(default=hordak.models.core.json_default, help_text='Original data received from the data source.', verbose_name='source data')),
                ('statement_import', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='hordak.statementimport', verbose_name='statement import')),
                ('transaction', models.ForeignKey(blank=True, default=None, help_text='Reconcile this statement line to this transaction', null=True, on_delete=django.db.models.deletion.SET_NULL, to='hordak.transaction', verbose_name='transaction')),
            ],
            options={
                'verbose_name': 'statementLine',
            },
        ),
        migrations.CreateModel(
            name='Leg',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='uuid')),
                ('amount_currency', djmoney.models.fields.CurrencyField(choices=[('XUA', 'ADB Unit of Account'), ('AFN', 'Afghan Afghani'), ('AFA', 'Afghan Afghani (1927–2002)'), ('ALL', 'Albanian Lek'), ('ALK', 'Albanian Lek (1946–1965)'), ('DZD', 'Algerian Dinar'), ('ADP', 'Andorran Peseta'), ('AOA', 'Angolan Kwanza'), ('AOK', 'Angolan Kwanza (1977–1991)'), ('AON', 'Angolan New Kwanza (1990–2000)'), ('AOR', 'Angolan Readjusted Kwanza (1995–1999)'), ('ARA', 'Argentine Austral'), ('ARS', 'Argentine Peso'), ('ARM', 'Argentine Peso (1881–1970)'), ('ARP', 'Argentine Peso (1983–1985)'), ('ARL', 'Argentine Peso Ley (1970–1983)'), ('AMD', 'Armenian Dram'), ('AWG', 'Aruban Florin'), ('AUD', 'Australian Dollar'), ('ATS', 'Austrian Schilling'), ('AZN', 'Azerbaijani Manat'), ('AZM', 'Azerbaijani Manat (1993–2006)'), ('BSD', 'Bahamian Dollar'), ('BHD', 'Bahraini Dinar'), ('BDT', 'Bangladeshi Taka'), ('BBD', 'Barbadian Dollar'), ('BYN', 'Belarusian Ruble'), ('BYB', 'Belarusian Ruble (1994–1999)'), ('BYR', 'Belarusian Ruble (2000–2016)'), ('BEF', 'Belgian Franc'), ('BEC', 'Belgian Franc (convertible)'), ('BEL', 'Belgian Franc (financial)'), ('BZD', 'Belize Dollar'), ('BMD', 'Bermudan Dollar'), ('BTN', 'Bhutanese Ngultrum'), ('BOB', 'Bolivian Boliviano'), ('BOL', 'Bolivian Boliviano (1863–1963)'), ('BOV', 'Bolivian Mvdol'), ('BOP', 'Bolivian Peso'), ('BAM', 'Bosnia-Herzegovina Convertible Mark'), ('BAD', 'Bosnia-Herzegovina Dinar (1992–1994)'), ('BAN', 'Bosnia-Herzegovina New Dinar (1994–1997)'), ('BWP', 'Botswanan Pula'), ('BRC', 'Brazilian Cruzado (1986–1989)'), ('BRZ', 'Brazilian Cruzeiro (1942–1967)'), ('BRE', 'Brazilian Cruzeiro (1990–1993)'), ('BRR', 'Brazilian Cruzeiro (1993–1994)'), ('BRN', 'Brazilian New Cruzado (1989–1990)'), ('BRB', 'Brazilian New Cruzeiro (1967–1986)'), ('BRL', 'Brazilian Real'), ('GBP', 'British Pound'), ('BND', 'Brunei Dollar'), ('BGL', 'Bulgarian Hard Lev'), ('BGN', 'Bulgarian Lev'), ('BGO', 'Bulgarian Lev (1879–1952)'), ('BGM', 'Bulgarian Socialist Lev'), ('BUK', 'Burmese Kyat'), ('BIF', 'Burundian Franc'), ('XPF', 'CFP Franc'), ('KHR', 'Cambodian Riel'), ('CAD', 'Canadian Dollar'), ('CVE', 'Cape Verdean Escudo'), ('KYD', 'Cayman Islands Dollar'), ('XAF', 'Central African CFA Franc'), ('CLE', 'Chilean Escudo'), ('CLP', 'Chilean Peso'), ('CLF', 'Chilean Unit of Account (UF)'), ('CNX', 'Chinese People’s Bank Dollar'), ('CNY', 'Chinese Yuan'), ('CNH', 'Chinese Yuan (offshore)'), ('COP', 'Colombian Peso'), ('COU', 'Colombian Real Value Unit'), ('KMF', 'Comorian Franc'), ('CDF', 'Congolese Franc'), ('CRC', 'Costa Rican Colón'), ('HRD', 'Croatian Dinar'), ('HRK', 'Croatian Kuna'), ('CUC', 'Cuban Convertible Peso'), ('CUP', 'Cuban Peso'), ('CYP', 'Cypriot Pound'), ('CZK', 'Czech Koruna'), ('CSK', 'Czechoslovak Hard Koruna'), ('DKK', 'Danish Krone'), ('DJF', 'Djiboutian Franc'), ('DOP', 'Dominican Peso'), ('NLG', 'Dutch Guilder'), ('XCD', 'East Caribbean Dollar'), ('DDM', 'East German Mark'), ('ECS', 'Ecuadorian Sucre'), ('ECV', 'Ecuadorian Unit of Constant Value'), ('EGP', 'Egyptian Pound'), ('GQE', 'Equatorial Guinean Ekwele'), ('ERN', 'Eritrean Nakfa'), ('EEK', 'Estonian Kroon'), ('ETB', 'Ethiopian Birr'), ('EUR', 'Euro'), ('XBA', 'European Composite Unit'), ('XEU', 'European Currency Unit'), ('XBB', 'European Monetary Unit'), ('XBC', 'European Unit of Account (XBC)'), ('XBD', 'European Unit of Account (XBD)'), ('FKP', 'Falkland Islands Pound'), ('FJD', 'Fijian Dollar'), ('FIM', 'Finnish Markka'), ('FRF', 'French Franc'), ('XFO', 'French Gold Franc'), ('XFU', 'French UIC-Franc'), ('GMD', 'Gambian Dalasi'), ('GEK', 'Georgian Kupon Larit'), ('GEL', 'Georgian Lari'), ('DEM', 'German Mark'), ('GHS', 'Ghanaian Cedi'), ('GHC', 'Ghanaian Cedi (1979–2007)'), ('GIP', 'Gibraltar Pound'), ('XAU', 'Gold'), ('GRD', 'Greek Drachma'), ('GTQ', 'Guatemalan Quetzal'), ('GWP', 'Guinea-Bissau Peso'), ('GNF', 'Guinean Franc'), ('GNS', 'Guinean Syli'), ('GYD', 'Guyanaese Dollar'), ('HTG', 'Haitian Gourde'), ('HNL', 'Honduran Lempira'), ('HKD', 'Hong Kong Dollar'), ('HUF', 'Hungarian Forint'), ('IMP', 'IMP'), ('ISK', 'Icelandic Króna'), ('ISJ', 'Icelandic Króna (1918–1981)'), ('INR', 'Indian Rupee'), ('IDR', 'Indonesian Rupiah'), ('IRR', 'Iranian Rial'), ('IQD', 'Iraqi Dinar'), ('IEP', 'Irish Pound'), ('ILS', 'Israeli New Shekel'), ('ILP', 'Israeli Pound'), ('ILR', 'Israeli Shekel (1980–1985)'), ('ITL', 'Italian Lira'), ('JMD', 'Jamaican Dollar'), ('JPY', 'Japanese Yen'), ('JOD', 'Jordanian Dinar'), ('KZT', 'Kazakhstani Tenge'), ('KES', 'Kenyan Shilling'), ('KWD', 'Kuwaiti Dinar'), ('KGS', 'Kyrgystani Som'), ('LAK', 'Laotian Kip'), ('LVL', 'Latvian Lats'), ('LVR', 'Latvian Ruble'), ('LBP', 'Lebanese Pound'), ('LSL', 'Lesotho Loti'), ('LRD', 'Liberian Dollar'), ('LYD', 'Libyan Dinar'), ('LTL', 'Lithuanian Litas'), ('LTT', 'Lithuanian Talonas'), ('LUL', 'Luxembourg Financial Franc'), ('LUC', 'Luxembourgian Convertible Franc'), ('LUF', 'Luxembourgian Franc'), ('MOP', 'Macanese Pataca'), ('MKD', 'Macedonian Denar'), ('MKN', 'Macedonian Denar (1992–1993)'), ('MGA', 'Malagasy Ariary'), ('MGF', 'Malagasy Franc'), ('MWK', 'Malawian Kwacha'), ('MYR', 'Malaysian Ringgit'), ('MVR', 'Maldivian Rufiyaa'), ('MVP', 'Maldivian Rupee (1947–1981)'), ('MLF', 'Malian Franc'), ('MTL', 'Maltese Lira'), ('MTP', 'Maltese Pound'), ('MRU', 'Mauritanian Ouguiya'), ('MRO', 'Mauritanian Ouguiya (1973–2017)'), ('MUR', 'Mauritian Rupee'), ('MXV', 'Mexican Investment Unit'), ('MXN', 'Mexican Peso'), ('MXP', 'Mexican Silver Peso (1861–1992)'), ('MDC', 'Moldovan Cupon'), ('MDL', 'Moldovan Leu'), ('MCF', 'Monegasque Franc'), ('MNT', 'Mongolian Tugrik'), ('MAD', 'Moroccan Dirham'), ('MAF', 'Moroccan Franc'), ('MZE', 'Mozambican Escudo'), ('MZN', 'Mozambican Metical'), ('MZM', 'Mozambican Metical (1980–2006)'), ('MMK', 'Myanmar Kyat'), ('NAD', 'Namibian Dollar'), ('NPR', 'Nepalese Rupee'), ('ANG', 'Netherlands Antillean Guilder'), ('TWD', 'New Taiwan Dollar'), ('NZD', 'New Zealand Dollar'), ('NIO', 'Nicaraguan Córdoba'), ('NIC', 'Nicaraguan Córdoba (1988–1991)'), ('NGN', 'Nigerian Naira'), ('KPW', 'North Korean Won'), ('NOK', 'Norwegian Krone'), ('OMR', 'Omani Rial'), ('PKR', 'Pakistani Rupee'), ('XPD', 'Palladium'), ('PAB', 'Panamanian Balboa'), ('PGK', 'Papua New Guinean Kina'), ('PYG', 'Paraguayan Guarani'), ('PEI', 'Peruvian Inti'), ('PEN', 'Peruvian Sol'), ('PES', 'Peruvian Sol (1863–1965)'), ('PHP', 'Philippine Piso'), ('XPT', 'Platinum'), ('PLN', 'Polish Zloty'), ('PLZ', 'Polish Zloty (1950–1995)'), ('PTE', 'Portuguese Escudo'), ('GWE', 'Portuguese Guinea Escudo'), ('QAR', 'Qatari Rial'), ('XRE', 'RINET Funds'), ('RHD', 'Rhodesian Dollar'), ('RON', 'Romanian Leu'), ('ROL', 'Romanian Leu (1952–2006)'), ('RUB', 'Russian Ruble'), ('RUR', 'Russian Ruble (1991–1998)'), ('RWF', 'Rwandan Franc'), ('SVC', 'Salvadoran Colón'), ('WST', 'Samoan Tala'), ('SAR', 'Saudi Riyal'), ('RSD', 'Serbian Dinar'), ('CSD', 'Serbian Dinar (2002–2006)'), ('SCR', 'Seychellois Rupee'), ('SLL', 'Sierra Leonean Leone'), ('XAG', 'Silver'), ('SGD', 'Singapore Dollar'), ('SKK', 'Slovak Koruna'), ('SIT', 'Slovenian Tolar'), ('SBD', 'Solomon Islands Dollar'), ('SOS', 'Somali Shilling'), ('ZAR', 'South African Rand'), ('ZAL', 'South African Rand (financial)'), ('KRH', 'South Korean Hwan (1953–1962)'), ('KRW', 'South Korean Won'), ('KRO', 'South Korean Won (1945–1953)'), ('SSP', 'South Sudanese Pound'), ('SUR', 'Soviet Rouble'), ('ESP', 'Spanish Peseta'), ('ESA', 'Spanish Peseta (A account)'), ('ESB', 'Spanish Peseta (convertible account)'), ('XDR', 'Special Drawing Rights'), ('LKR', 'Sri Lankan Rupee'), ('SHP', 'St. Helena Pound'), ('XSU', 'Sucre'), ('SDD', 'Sudanese Dinar (1992–2007)'), ('SDG', 'Sudanese Pound'), ('SDP', 'Sudanese Pound (1957–1998)'), ('SRD', 'Surinamese Dollar'), ('SRG', 'Surinamese Guilder'), ('SZL', 'Swazi Lilangeni'), ('SEK', 'Swedish Krona'), ('CHF', 'Swiss Franc'), ('SYP', 'Syrian Pound'), ('STN', 'São Tomé & Príncipe Dobra'), ('STD', 'São Tomé & Príncipe Dobra (1977–2017)'), ('TVD', 'TVD'), ('TJR', 'Tajikistani Ruble'), ('TJS', 'Tajikistani Somoni'), ('TZS', 'Tanzanian Shilling'), ('XTS', 'Testing Currency Code'), ('THB', 'Thai Baht'), ('XXX', 'The codes assigned for transactions where no currency is involved'), ('TPE', 'Timorese Escudo'), ('TOP', 'Tongan Paʻanga'), ('TTD', 'Trinidad & Tobago Dollar'), ('TND', 'Tunisian Dinar'), ('TRY', 'Turkish Lira'), ('TRL', 'Turkish Lira (1922–2005)'), ('TMT', 'Turkmenistani Manat'), ('TMM', 'Turkmenistani Manat (1993–2009)'), ('USD', 'US Dollar'), ('USN', 'US Dollar (Next day)'), ('USS', 'US Dollar (Same day)'), ('UGX', 'Ugandan Shilling'), ('UGS', 'Ugandan Shilling (1966–1987)'), ('UAH', 'Ukrainian Hryvnia'), ('UAK', 'Ukrainian Karbovanets'), ('AED', 'United Arab Emirates Dirham'), ('UYW', 'Uruguayan Nominal Wage Index Unit'), ('UYU', 'Uruguayan Peso'), ('UYP', 'Uruguayan Peso (1975–1993)'), ('UYI', 'Uruguayan Peso (Indexed Units)'), ('UZS', 'Uzbekistani Som'), ('VUV', 'Vanuatu Vatu'), ('VES', 'Venezuelan Bolívar'), ('VEB', 'Venezuelan Bolívar (1871–2008)'), ('VEF', 'Venezuelan Bolívar (2008–2018)'), ('VND', 'Vietnamese Dong'), ('VNN', 'Vietnamese Dong (1978–1985)'), ('CHE', 'WIR Euro'), ('CHW', 'WIR Franc'), ('XOF', 'West African CFA Franc'), ('YDD', 'Yemeni Dinar'), ('YER', 'Yemeni Rial'), ('YUN', 'Yugoslavian Convertible Dinar (1990–1992)'), ('YUD', 'Yugoslavian Hard Dinar (1966–1990)'), ('YUM', 'Yugoslavian New Dinar (1994–2002)'), ('YUR', 'Yugoslavian Reformed Dinar (1992–1993)'), ('ZWN', 'ZWN'), ('ZRN', 'Zairean New Zaire (1993–1998)'), ('ZRZ', 'Zairean Zaire (1971–1993)'), ('ZMW', 'Zambian Kwacha'), ('ZMK', 'Zambian Kwacha (1968–2012)'), ('ZWD', 'Zimbabwean Dollar (1980–2008)'), ('ZWR', 'Zimbabwean Dollar (2008)'), ('ZWL', 'Zimbabwean Dollar (2009)')], default='EUR', editable=False, max_length=3)),
                ('amount', djmoney.models.fields.MoneyField(decimal_places=2, default_currency='EUR', help_text='Record debits as positive, credits as negative', max_digits=13, verbose_name='amount')),
                ('description', models.TextField(blank=True, default='', verbose_name='description')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='legs', to='hordak.account', verbose_name='account')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='legs', to='hordak.transaction', verbose_name='transaction')),
            ],
            options={
                'verbose_name': 'Leg',
            },
        ),
        migrations.CreateModel(
            name='TransactionCsvImportColumn',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('column_number', models.PositiveSmallIntegerField(verbose_name='column number')),
                ('column_heading', models.CharField(blank=True, default='', max_length=100, verbose_name='Column')),
                ('to_field', models.CharField(blank=True, choices=[(None, '-- Do not import --'), ('date', 'Date'), ('amount', 'Amount'), ('amount_out', 'Amount (money out only)'), ('amount_in', 'Amount (money in only)'), ('description', 'Description / Notes')], default=None, max_length=20, null=True, verbose_name='Is')),
                ('example', models.CharField(blank=True, default='', max_length=200, verbose_name='example')),
                ('transaction_import', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='columns', to='hordak.transactioncsvimport', verbose_name='transaction import')),
            ],
            options={
                'verbose_name': 'transactionCsvImportColumn',
                'ordering': ['transaction_import', 'column_number'],
                'unique_together': {('transaction_import', 'column_number'), ('transaction_import', 'to_field')},
            },
        ),
    ]
