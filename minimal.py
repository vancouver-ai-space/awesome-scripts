import graphviz

# Define the graphviz string for the ITSM Ticket Workflow
workflow_dot = """
digraph ITSM_Ticket_Workflow {
    rankdir=LR;
    node [shape=rectangle];

    Start [label="Start"];
    Raise_Ticket [label="Raise Ticket"];
    Assign_To_Group [label="Assign to Group"];
    Technician_Assignment [label="Technician Assignment"];
    Work_In_Progress [label="Work in Progress"];
    Resolve_Ticket [label="Resolve Ticket"];
    Validate_Resolution [label="Validate Resolution"];
    Close_Ticket [label="Close Ticket"];
    Escalate [label="Escalate"];

    Start -> Raise_Ticket;
    Raise_Ticket -> Assign_To_Group;
    Assign_To_Group -> Technician_Assignment;
    Technician_Assignment -> Work_In_Progress;
    Work_In_Progress -> Resolve_Ticket;
    Resolve_Ticket -> Validate_Resolution;
    Validate_Resolution -> Close_Ticket [label="Validated"];
    Validate_Resolution -> Escalate [label="Not Validated"];
    Escalate -> Technician_Assignment;
}
"""

# Render the graph
workflow_graph = graphviz.Source(workflow_dot)
workflow_graph.view("ITSM_Ticket_Workflow")
