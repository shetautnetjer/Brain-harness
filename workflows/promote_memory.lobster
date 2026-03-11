workflow promote_memory {
  step collect_plane_a_packet
  step arbiter_tag_ruling
  step enforce_source_events_gate
  step write_plane_b_canonical
  step emit_promotion_audit
}
