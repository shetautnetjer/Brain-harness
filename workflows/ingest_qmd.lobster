workflow ingest_qmd {
  step parse_frontmatter using qmd_guard
  step validate_identity
  step validate_tags
  step validate_provenance
  step route_plane
  step write_or_emit_violation
}
