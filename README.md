# French Company Snapshot & Change Check

Fetch a public company snapshot from the official French Recherche d’entreprises API and optionally compare it with a previous snapshot hash.

## Input

Provide 1–100 nine-digit SIRENs. Duplicate SIRENs are deduplicated. `previousHashes` is an optional map from SIREN to a SHA-256 snapshot hash.

```json
{
  "sirens": ["552032534"],
  "previousHashes": {}
}
```

To check for changes on a later run, pass the `snapshotHash` returned for each SIREN in `previousHashes`. On the first run, `changed` is `null`. On later runs, it reports the comparison with the explicitly supplied previous hash; the Actor does not retain shared state.

## Results

Every result includes `siren`, `checkedAt`, `sourceUrl` and a status. Found results include a `company` object with `siren`, `nom_complet`, `etat_administratif`, `activite_principale`, `nature_juridique`, plus `snapshotHash` and `changed`.

Statuses are `found`, `not_found`, `source_unavailable`, and `excluded_non_company_or_non_public`. Only commercial legal entities with a `nature_juridique` beginning with `5` and `statut_diffusion` equal to `O` are eligible. `O` marks data as publicly disseminated; it does not indicate that the company is active.

The Actor makes requests at one per second. It does not return people, directors, addresses, emails, phone numbers, or financial data. It is not a legal or credit certification, and source availability is not guaranteed.

## Pricing

Pay per event: $3 per 1,000 eligible company snapshots ($0.003 each), with platform usage included. The `company-snapshot` event applies only to an eligible company with status `found`; missing, excluded, or unavailable results are not charged. There is no separate start fee or automatic dataset-item fee. Consult the Store pricing tab for current terms.

## License and data

Code: MIT. Source data is subject to the official API’s terms: https://recherche-entreprises.api.gouv.fr/search?minimal=true

Reda – Frix Studio
