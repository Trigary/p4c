
struct ethernet_t {
	bit<48> dstAddr
	bit<48> srcAddr
	bit<16> etherType
}

struct psa_ingress_output_metadata_t {
	bit<8> class_of_service
	bit<8> clone
	bit<16> clone_session_id
	bit<8> drop
	bit<8> resubmit
	bit<32> multicast_group
	bit<32> egress_port
}

struct psa_egress_output_metadata_t {
	bit<8> clone
	bit<16> clone_session_id
	bit<8> drop
}

struct psa_egress_deparser_input_metadata_t {
	bit<32> egress_port
}

struct EMPTY_M {
	bit<32> psa_ingress_input_metadata_ingress_port
	bit<8> psa_ingress_output_metadata_drop
	bit<32> psa_ingress_output_metadata_egress_port
}
metadata instanceof EMPTY_M

header ethernet instanceof ethernet_t

action NoAction args none {
	return
}

action remove_header args none {
	invalidate h.ethernet
	return
}

table tbl {
	key {
		h.ethernet.srcAddr exact
	}
	actions {
		NoAction
		remove_header
	}
	default_action NoAction args none 
	size 0x10000
}


apply {
	rx m.psa_ingress_input_metadata_ingress_port
	mov m.psa_ingress_output_metadata_drop 0x0
	extract h.ethernet
	table tbl
	jmpnh LABEL_END
	invalidate h.ethernet
	LABEL_END :	table tbl
	jmpnh LABEL_FALSE_0
	jmp LABEL_END_0
	LABEL_FALSE_0 :	validate h.ethernet
	LABEL_END_0 :	table tbl
	jmpnh LABEL_FALSE_1
	jmp LABEL_END_1
	LABEL_FALSE_1 :	validate h.ethernet
	LABEL_END_1 :	table tbl
	jmpnh LABEL_END_2
	invalidate h.ethernet
	LABEL_END_2 :	jmpneq LABEL_DROP m.psa_ingress_output_metadata_drop 0x0
	tx m.psa_ingress_output_metadata_egress_port
	LABEL_DROP :	drop
}


