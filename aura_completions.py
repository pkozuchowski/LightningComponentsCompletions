import sublime, sublime_plugin
import re


def match(rex, str):
    m = rex.match(str)
    if m:
        return m.group(0)
    else:
        return None

def make_completion(tag):
    # make it look like
    # ("table\tTag", "table>$1</table>"),
    return (tag + '\tTag', tag + ' $0 ></' + tag + '>')

def get_tag_to_attributes():
    """
    Returns a dictionary with attributes accociated to tags
    This assumes that all tags can have global attributes as per MDN:
    https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes
    """

    # Map tags to specific attributes applicable for that tag
    tag_dict = {
        'aura:attribute' : {
            'name':'String', 
            'type':'String', 
            'access':'String',
            'default':'String',
            'required':'Boolean',
            'description':'String'},

        'aura:if' : {'isTrue':'Boolean'},

        'aura:iteration': {
            'items': 'List',
            'var': 'String',
            'indexVar': 'String',
            'start': 'Integer',
            'end': 'Integer',
            'loaded': 'Boolean',
            'body': 'Componentdefref[]',
            'template': 'Componentdefref[]'},

        'aura:set': {
            'attribute':'String',
            'value':'Object'},

        'aura:event':{
            'type' : 'String'
        },

        'aura:registerEvent' :{
            'name': 'String',
            'type': 'String'},

        'aura:handler': {
            'name':'String',
            'event':'Event',
            'action':'Method',
            'value':'Object'},
        
        'aura:component' : {
            'access':'String', 
            'controller':'String', 
            'description':'String',
            'extends':'Component',
            'extensible':'Boolean',
            'implements':'String',
            'isTemplate':'Boolean'},

        'aura:dependency' : {
                    'resource':'String', 
                    'type':'String'},

        'aura:interface' : {
                    'access':'String',
                    'description':'String',
                    'extends':'Component'},

        'aura:method' : {
                    'name':'String', 
                    'action':'Expression',
                    'access':'String',
                    'description':'String'},

        'aura:expression' : {'value' :'String'},

        'aura:html' : {
                    'body':'Component[]', 
                    'HTMLAttributes':'Map', 
                    'tag':'String'},

        'aura:renderif' : {'isTrue':'Boolean'},

        'aura:unescapedHtml' : {'value':'String'},

        'auraStorage:init' : {
                    'clearStorageOnInit':'Boolean', 
                    'debugLoggingEnabled':'Boolean', 
                    'defaultAutoRefreshInterval':'Integer',
                    'defaultExpiration':'Integer',
                    'maxSize':'Integer',
                    'name':'String',
                    'persistent':'Boolean',
                    'secure':'Boolean',
                    'version':'String'},

        'force:canvasApp' : {
                    'applicationName':'String', 
                    'border':'String', 
                    'canvasId':'String',
                    'containerId':'String',
                    'developerName':'String',
                    'displayLocation':'String',
                    'height':'String',
                    'maxHeight':'String',
                    'maxWidth':'String',
                    'namespacePrefix':'String',
                    'onCanvasAppError':'String',
                    'onCanvasAppLoad':'String',
                    'onCanvasSubscribed':'String',
                    'parameters':'String',
                    'referenceId':'Id',
                    'scrolling':'String',
                    'sublocation':'String',
                    'title':'String',
                    'watermark':'Boolean',
                    'width':'String'},

        'force:inputField' : {
                    'class':'String', 
                    'required':'Boolean',
                    'value':'Object',
                    'change':'Component'},

        'force:outputField' : {
                    'class':'String', 
                    'value':'Object'},

        'force:recordEdit' : {
                    'recordId':'String', 
                    'recordSave':'Component',
                    'onSaveSuccess':'Component'},

        'force:recordView' : {
                    'record':'SObjectRow', 
                    'recordId':'String',
                    'type':'String'},

        'forceChatter:feed' : {
                    'feedDesign':'String', 
                    'subjectId':'String',
                    'type':'String'},

        'forceChatter:fullFeed' : {
                    'handleNavigationEvents':'Boolean', 
                    'subjectId':'String',
                    'type':'String'},

        'forceChatter:publisher' : {
                    'context':'String', 
                    'recordId':'String'},

        'lightning:badge' : {
                    'class':'String',
                    'label':'String'},

        'lightning:button' : {
                    'class':'String', 
                    'disabled':'Boolean',
                    'iconName':'String',
                    'iconPosition':'String',
                    'label':'String',
                    'name':'String',
                    'onblur':'Action',
                    'onclick':'Action',
                    'onfocus':'Action',
                    'tabindex':'Integer',
                    'value':'String',
                    'variant':'String'},

        'lightning:buttonGroup' : {'class':'String'},

        'lightning:buttonIcon' : {
                    'accesskey':'String',
                    'alternativeText':'String',
                    'class':'String', 
                    'disabled':'Boolean',
                    'iconName':'String',
                    'name':'String',
                    'onblur':'Action',
                    'onclick':'Action',
                    'onfocus':'Action',
                    'size':'String',
                    'tabindex':'Integer',
                    'value':'String',
                    'variant':'String'},

        'lightning:buttonMenu' : {
                    'accesskey':'String',
                    'alternativeText':'String',
                    'class':'String', 
                    'disabled':'Boolean',
                    'iconName':'String',
                    'iconSize':'String',
                    'menuAlignment':'String',
                    'name':'String',
                    'onblur':'Action',
                    'onselect':'Action',
                    'onfocus':'Action',
                    'title':'String',
                    'tabindex':'Integer',
                    'value':'String',
                    'variant':'String',
                    'visible':'Boolean'},

        'lightning:card' : {
                    'actions':'Component[]',
                    'class':'String', 
                    'footer':'Component[]',
                    'iconName':'String',
                    'title':'Component[]',
                    'variant':'String'},

        'lightning:formattedDateTime' : {
                    'day':'String',
                    'era':'String',
                    'hour':'String', 
                    'hour12':'Boolean',
                    'minute':'String',
                    'month':'String',
                    'second':'String',
                    'timeZone':'String',
                    'timeZoneName':'String',
                    'value':'Object',
                    'weekday':'String',
                    'year':'String'},

        'lightning:formattedNumber' : {
                    'currencyCode':'String',
                    'currencyDisplayAs':'String',
                    'maximumFractionDigits':'Integer', 
                    'maximumSignificantDigits':'Integer',
                    'minimumFractionDigits':'Integer',
                    'minimumIntegerDigits':'Integer',
                    'minimumSignificantDigits':'Integer',
                    'style':'String',
                    'value':'Decimal'},

        'lightning:icon' : {
                    'alternativeText':'String',
                    'class':'String', 
                    'iconName':'String',
                    'size':'String',
                    'variant':'String'},

        'lightning:Input' : {
                    'accesskey':'String',
                    'checked':'Boolean',
                    'class':'String', 
                    'disabled':'Boolean',
                    'formatter':'String',
                    'label':'String',
                    'max':'Decimal',
                    'maxLength':'Integer',
                    'messageWhenBadInput':'String',
                    'messageWhenPatternMismatch':'String',
                    'messageWhenRangeOverflow':'String',
                    'messageWhenRangeUnderflow':'String',
                    'messageWhenStepMismatch':'String',
                    'messageWhenTooLong':'String',
                    'messageWhenTypeMismatch':'String',
                    'messageWhenValueMissing':'String',
                    'min':'Decimal',
                    'minlength':'Integer',
                    'name':'String',
                    'onblur':'Action',
                    'onchange':'Action',
                    'onfocus':'Action',
                    'pattern':'String',
                    'placeholder':'String',
                    'readonly':'Boolean',
                    'required':'Boolean',
                    'step':'Object',
                    'tabindex':'Integer',
                    'type':'String',
                    'validity':'Object',
                    'value':'Object'},


        'lightning:layout' : {
                    'class':'String', 
                    'horizontalAlign':'String',
                    'multipleRows':'Boolean',
                    'pullToBoundary':'Boolean',
                    'verticalAlign':'String'},


        'lightning:layoutItem' : {
                    'class':'String', 
                    'flexibility':'Object',
                    'largeDeviceSize':'Integer',
                    'mediumDeviceSize':'Integer',
                    'smallDeviceSize':'Integer',
                    'padding':'String',
                    'size':'Integer'},


        'lightning:menuItem' : {
                    'accesskey':'String',
                    'checked':'Boolean',
                    'class':'String', 
                    'disabled':'Boolean',
                    'iconName':'String',
                    'label':'String',
                    'onblur':'Action',
                    'onfocus':'Action',
                    'tabindex':'Integer',
                    'title':'String',
                    'value':'String'},


        'lightning:select' : {
                    'accesskey':'String',
                    'class':'String', 
                    'disabled':'Boolean',
                    'label':'String',
                    'messageWhenValueMissing':'String',
                    'name':'String',
                    'onblur':'Action',
                    'onfocus':'Action',
                    'onchange':'Action',
                    'readonly':'Boolean',
                    'required':'Boolean',
                    'tabindex':'Integer',
                    'validity':'Object',
                    'value':'String'},

        'lightning:spinner' : {
                    'class':'String',
                    'size':'String',
                    'variant':'String'},

        'lightning:tab' : {
                    'accesskey':'String',
                    'id':'String', 
                    'onblur':'Action',
                    'onfocus':'Action',
                    'tabindex':'Integer',
                    'title':'String'},

        'lightning:tabset' : {
                    'class':'String', 
                    'onselect':'Action',
                    'selectedTabid':'String',
                    'variant':'String'},

        'lightning:textarea' : {
                    'accesskey':'String',
                    'class':'String', 
                    'disabled':'Boolean',
                    'label':'String',
                    'maxLength':'Integer',
                    'messageWhenBadInput':'String',
                    'messageWhenTooLong':'String',
                    'messageWhenValueMissing':'String',
                    'minlength':'Integer',
                    'name':'String',
                    'onblur':'Action',
                    'onchange':'Action',
                    'onfocus':'Action',
                    'placeholder':'String',
                    'readonly':'Boolean',
                    'required':'Boolean',
                    'tabindex':'Integer',
                    'validity':'Object',
                    'value':'Object'},

        'ltng:require' : {
                    'scripts':'String[]',
                    'styles':'String[]',
                    'afterScriptsLoaded':'COMPONENT',
                    'beforeLoadingResources':'COMPONENT'},

        'ui:actionMenuItem' : {
                    'class':'String',
                    'disabled':'Boolean',
                    'hideMenuAfterSelected':'Boolean',
                    'label':'String',
                    'selected':'Boolean',
                    'type':'String',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'select':'COMPONENT',
                    'blur':'COMPONENT',
                    'keypress':'COMPONENT',
                    'keyup':'COMPONENT',
                    'keydown':'COMPONENT'},

        'ui:button' : {
                    'accesskey':'String',
                    'buttonTitle':'String',
                    'buttonType':'String',
                    'class':'String',
                    'disabled':'Boolean',
                    'label':'String',
                    'labelClass':'String',
                    'press':'COMPONENT'},

        'ui:checkboxMenuItem' : {
                    'class':'String',
                    'disabled':'Boolean',
                    'hideMenuAfterSelected':'Boolean',
                    'label':'String',
                    'selected':'Boolean',
                    'type':'String',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT',
                    'select':'COMPONENT',
                    'blur':'COMPONENT',
                    'focus':'COMPONENT',
                    'keypress':'COMPONENT',
                    'keyup':'COMPONENT',
                    'keydown':'COMPONENT'},

        'ui:inputCheckbox' : {
                    'class':'String',
                    'disabled':'Boolean',
                    'errors':'List',
                    'label':'String',
                    'labelClass':'String',
                    'name':'String',
                    'required':'Boolean',
                    'requiredIndicatorClass':'String',
                    'text':'String',
                    'updateOn':'String',
                    'value':'Boolean',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT',
                    'select':'COMPONENT',
                    'blur':'COMPONENT',
                    'focus':'COMPONENT',
                    'keypress':'COMPONENT',
                    'keyup':'COMPONENT',
                    'keydown':'COMPONENT',
                    'cut':'COMPONENT',
                    'onError':'COMPONENT',
                    'onClearErrors':'COMPONENT',
                    'change':'COMPONENT',
                    'copy':'COMPONENT',
                    'paste':'COMPONENT'},

        'ui:inputCurrency' : {
                    'class':'String',
                    'disabled':'Boolean',
                    'errors':'List',
                    'format':'String',
                    'label':'String',
                    'labelClass':'String',
                    'maxlength':'Integer',
                    'placeholder':'String',
                    'required':'Boolean',
                    'requiredIndicatorClass':'String',
                    'size':'Integer',
                    'updateOn':'String',
                    'value':'Boolean',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT',
                    'select':'COMPONENT',
                    'blur':'COMPONENT',
                    'focus':'COMPONENT',
                    'keypress':'COMPONENT',
                    'keyup':'COMPONENT',
                    'keydown':'COMPONENT',
                    'cut':'COMPONENT',
                    'onError':'COMPONENT',
                    'onClearErrors':'COMPONENT',
                    'change':'COMPONENT',
                    'copy':'COMPONENT',
                    'paste':'COMPONENT'},

        'ui:inputDate' : {
                    'class':'String',
                    'disabled':'Boolean',
                    'errors':'List',
                    'displayDatePicker':'Boolean',
                    'format':'String',
                    'label':'String',
                    'labelClass':'String',
                    'langLocale':'String',
                    'required':'Boolean',
                    'requiredIndicatorClass':'String',
                    'updateOn':'String',
                    'value':'Boolean',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT',
                    'select':'COMPONENT',
                    'blur':'COMPONENT',
                    'focus':'COMPONENT',
                    'keypress':'COMPONENT',
                    'keyup':'COMPONENT',
                    'keydown':'COMPONENT',
                    'cut':'COMPONENT',
                    'onError':'COMPONENT',
                    'onClearErrors':'COMPONENT',
                    'change':'COMPONENT',
                    'copy':'COMPONENT',
                    'paste':'COMPONENT'},

        'ui:inputDateTime' : {
                    'class':'String',
                    'disabled':'Boolean',
                    'errors':'List',
                    'displayDatePicker':'Boolean',
                    'format':'String',
                    'label':'String',
                    'labelClass':'String',
                    'langLocale':'String',
                    'required':'Boolean',
                    'requiredIndicatorClass':'String',
                    'updateOn':'String',
                    'value':'Boolean',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT',
                    'select':'COMPONENT',
                    'blur':'COMPONENT',
                    'focus':'COMPONENT',
                    'keypress':'COMPONENT',
                    'keyup':'COMPONENT',
                    'keydown':'COMPONENT',
                    'cut':'COMPONENT',
                    'onError':'COMPONENT',
                    'onClearErrors':'COMPONENT',
                    'change':'COMPONENT',
                    'copy':'COMPONENT',
                    'paste':'COMPONENT'},

        'ui:inputDefaultError' : {
                    'class':'String',
                    'value':'String[]',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT'},

        'ui:inputEmail' : {
                    'class':'String',
                    'disabled':'Boolean',
                    'errors':'List',
                    'label':'String',
                    'labelClass':'String',
                    'maxlength':'Integer',
                    'placeholder':'String',
                    'required':'Boolean',
                    'requiredIndicatorClass':'String',
                    'size':'Integer',
                    'updateOn':'String',
                    'value':'Boolean',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT',
                    'select':'COMPONENT',
                    'blur':'COMPONENT',
                    'focus':'COMPONENT',
                    'keypress':'COMPONENT',
                    'keyup':'COMPONENT',
                    'keydown':'COMPONENT',
                    'cut':'COMPONENT',
                    'onError':'COMPONENT',
                    'onClearErrors':'COMPONENT',
                    'change':'COMPONENT',
                    'copy':'COMPONENT',
                    'paste':'COMPONENT'},

        'ui:inputNumber' : {
                    'class':'String',
                    'disabled':'Boolean',
                    'errors':'List',
                    'format':'String',
                    'label':'String',
                    'labelClass':'String',
                    'maxlength':'Integer',
                    'placeholder':'String',
                    'required':'Boolean',
                    'requiredIndicatorClass':'String',
                    'size':'Integer',
                    'updateOn':'String',
                    'value':'Boolean',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT',
                    'select':'COMPONENT',
                    'blur':'COMPONENT',
                    'focus':'COMPONENT',
                    'keypress':'COMPONENT',
                    'keyup':'COMPONENT',
                    'keydown':'COMPONENT',
                    'cut':'COMPONENT',
                    'onError':'COMPONENT',
                    'onClearErrors':'COMPONENT',
                    'change':'COMPONENT',
                    'copy':'COMPONENT',
                    'paste':'COMPONENT'},

        'ui:inputPhone' : {
                    'class':'String',
                    'disabled':'Boolean',
                    'errors':'List',
                    'label':'String',
                    'labelClass':'String',
                    'maxlength':'Integer',
                    'placeholder':'String',
                    'required':'Boolean',
                    'requiredIndicatorClass':'String',
                    'size':'Integer',
                    'updateOn':'String',
                    'value':'Boolean',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT',
                    'select':'COMPONENT',
                    'blur':'COMPONENT',
                    'focus':'COMPONENT',
                    'keypress':'COMPONENT',
                    'keyup':'COMPONENT',
                    'keydown':'COMPONENT',
                    'cut':'COMPONENT',
                    'onError':'COMPONENT',
                    'onClearErrors':'COMPONENT',
                    'change':'COMPONENT',
                    'copy':'COMPONENT',
                    'paste':'COMPONENT'},

        'ui:inputRadio' : {
                    'class':'String',
                    'disabled':'Boolean',
                    'errors':'List',
                    'label':'String',
                    'labelClass':'String',
                    'name':'String',
                    'text':'String',
                    'required':'Boolean',
                    'requiredIndicatorClass':'String',
                    'updateOn':'String',
                    'value':'Boolean',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT',
                    'select':'COMPONENT',
                    'blur':'COMPONENT',
                    'focus':'COMPONENT',
                    'keypress':'COMPONENT',
                    'keyup':'COMPONENT',
                    'keydown':'COMPONENT',
                    'cut':'COMPONENT',
                    'onError':'COMPONENT',
                    'onClearErrors':'COMPONENT',
                    'change':'COMPONENT',
                    'copy':'COMPONENT',
                    'paste':'COMPONENT'},

        'ui:inputRichText' : {
                    'class':'String',
                    'cols':'Integer',
                    'disabled':'Boolean',
                    'errors':'ArrayList',
                    'height':'String',
                    'label':'String',
                    'labelClass':'String',
                    'maxlength':'Integer',
                    'placeholder':'String',
                    'readonly':'Boolean',
                    'required':'Boolean',
                    'requiredIndicatorClass':'String',
                    'resizable':'Boolean',
                    'rows':'Integer',
                    'updateOn':'String',
                    'value':'Boolean',
                    'width':'String',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT',
                    'select':'COMPONENT',
                    'blur':'COMPONENT',
                    'focus':'COMPONENT',
                    'keypress':'COMPONENT',
                    'keyup':'COMPONENT',
                    'keydown':'COMPONENT',
                    'cut':'COMPONENT',
                    'onError':'COMPONENT',
                    'onClearErrors':'COMPONENT',
                    'change':'COMPONENT',
                    'copy':'COMPONENT',
                    'paste':'COMPONENT'},

        'ui:inputSecret' : {
                    'class':'String',
                    'disabled':'Boolean',
                    'errors':'List',
                    'label':'String',
                    'labelClass':'String',
                    'maxlength':'Integer',
                    'placeholder':'String',
                    'required':'Boolean',
                    'requiredIndicatorClass':'String',
                    'size':'Integer',
                    'updateOn':'String',
                    'value':'Boolean',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT',
                    'select':'COMPONENT',
                    'blur':'COMPONENT',
                    'focus':'COMPONENT',
                    'keypress':'COMPONENT',
                    'keyup':'COMPONENT',
                    'keydown':'COMPONENT',
                    'cut':'COMPONENT',
                    'onError':'COMPONENT',
                    'onClearErrors':'COMPONENT',
                    'change':'COMPONENT',
                    'copy':'COMPONENT',
                    'paste':'COMPONENT'},

        'ui:inputSelect' : {
                    'class':'String',
                    'disabled':'Boolean',
                    'errors':'List',
                    'label':'String',
                    'labelClass':'String',
                    'multiple':'Boolean',
                    'options':'List',
                    'required':'Boolean',
                    'requiredIndicatorClass':'String',
                    'updateOn':'String',
                    'value':'Boolean',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT',
                    'select':'COMPONENT',
                    'blur':'COMPONENT',
                    'focus':'COMPONENT',
                    'keypress':'COMPONENT',
                    'keyup':'COMPONENT',
                    'keydown':'COMPONENT',
                    'cut':'COMPONENT',
                    'onError':'COMPONENT',
                    'onClearErrors':'COMPONENT',
                    'change':'COMPONENT',
                    'copy':'COMPONENT',
                    'paste':'COMPONENT'},

        'ui:inputSelectOption' : {
                    'class':'String',
                    'disabled':'Boolean',
                    'label':'String',
                    'name':'String',
                    'text':'String',
                    'value':'Boolean',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT',
                    'select':'COMPONENT',
                    'blur':'COMPONENT',
                    'focus':'COMPONENT',
                    'keypress':'COMPONENT',
                    'keyup':'COMPONENT',
                    'keydown':'COMPONENT'},

        'ui:inputText' : {
                    'class':'String',
                    'disabled':'Boolean',
                    'errors':'List',
                    'label':'String',
                    'labelClass':'String',
                    'maxlength':'Integer',
                    'placeholder':'String',
                    'required':'Boolean',
                    'requiredIndicatorClass':'String',
                    'size':'Integer',
                    'updateOn':'String',
                    'value':'Boolean',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT',
                    'select':'COMPONENT',
                    'blur':'COMPONENT',
                    'focus':'COMPONENT',
                    'keypress':'COMPONENT',
                    'keyup':'COMPONENT',
                    'keydown':'COMPONENT',
                    'cut':'COMPONENT',
                    'onError':'COMPONENT',
                    'onClearErrors':'COMPONENT',
                    'change':'COMPONENT',
                    'copy':'COMPONENT',
                    'paste':'COMPONENT'},

        'ui:inputTextArea' : {
                    'class':'String',
                    'cols':'Integer',
                    'disabled':'Boolean',
                    'errors':'List',
                    'label':'String',
                    'labelClass':'String',
                    'maxlength':'Integer',
                    'placeholder':'String',
                    'readonly':'Boolean',
                    'required':'Boolean',
                    'requiredIndicatorClass':'String',
                    'resizable':'Boolean',
                    'rows':'Integer',
                    'updateOn':'String',
                    'value':'Boolean',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT',
                    'select':'COMPONENT',
                    'blur':'COMPONENT',
                    'focus':'COMPONENT',
                    'keypress':'COMPONENT',
                    'keyup':'COMPONENT',
                    'keydown':'COMPONENT',
                    'cut':'COMPONENT',
                    'onError':'COMPONENT',
                    'onClearErrors':'COMPONENT',
                    'change':'COMPONENT',
                    'copy':'COMPONENT',
                    'paste':'COMPONENT'},

        'ui:inputURL' : {
                    'class':'String',
                    'disabled':'Boolean',
                    'errors':'List',
                    'label':'String',
                    'labelClass':'String',
                    'maxlength':'Integer',
                    'placeholder':'String',
                    'required':'Boolean',
                    'requiredIndicatorClass':'String',
                    'size':'Integer',
                    'updateOn':'String',
                    'value':'Boolean',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT',
                    'select':'COMPONENT',
                    'blur':'COMPONENT',
                    'focus':'COMPONENT',
                    'keypress':'COMPONENT',
                    'keyup':'COMPONENT',
                    'keydown':'COMPONENT',
                    'cut':'COMPONENT',
                    'onError':'COMPONENT',
                    'onClearErrors':'COMPONENT',
                    'change':'COMPONENT',
                    'copy':'COMPONENT',
                    'paste':'COMPONENT'},

        'ui:menu' : {
                    'class':'String',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT'},

        'ui:menuItem' : {
                    'class':'String',
                    'disabled':'Boolean',
                    'hideMenuAfterSelected':'Boolean',
                    'label':'String',
                    'selected':'Boolean',
                    'type':'String',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT',
                    'select':'COMPONENT',
                    'blur':'COMPONENT',
                    'focus':'COMPONENT',
                    'keypress':'COMPONENT',
                    'keyup':'COMPONENT',
                    'keydown':'COMPONENT'},

        'ui:menuItemSeparator' : {
                    'class':'String',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT'},

        'ui:menuList' : {
                    'autoPosition':'Boolean',
                    'class':'String',
                    'closeOnClickOutside':'Boolean',
                    'closeOnTabKey':'Boolean',
                    'menuItems':'List',
                    'visible':'Boolean',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT',
                    'menuExpand':'COMPONENT',
                    'menuSelect':'COMPONENT',
                    'menuCollapse':'COMPONENT',
                    'menuFocusChange':'COMPONENT'},

        'ui:menuTrigger' : {
                    'class':'String',
                    'disabled':'Boolean',
                    'title':'String',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT',
                    'select':'COMPONENT',
                    'blur':'COMPONENT',
                    'focus':'COMPONENT',
                    'keypress':'COMPONENT',
                    'keyup':'COMPONENT',
                    'keydown':'COMPONENT',
                    'menuTriggerPress':'COMPONENT'},

        'ui:menuTriggerLink' : {
                    'class':'String',
                    'disabled':'Boolean',
                    'label':'String',
                    'title':'String',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT',
                    'select':'COMPONENT',
                    'blur':'COMPONENT',
                    'focus':'COMPONENT',
                    'keypress':'COMPONENT',
                    'keyup':'COMPONENT',
                    'keydown':'COMPONENT',
                    'menuTriggerPress':'COMPONENT'},

        'ui:message' : {
                    'class':'String',
                    'closable':'Boolean',
                    'severity':'String',
                    'title':'String',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT'},

        'ui:outputCheckbox' : {
                    'altChecked':'String',
                    'altUnchecked':'String',
                    'class':'String',
                    'value':'Boolean',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT'},

        'ui:outputCurrency' : {
                    'class':'String',
                    'currencyCode':'String',
                    'currencySymbol':'String',
                    'format':'String',
                    'value':'BigDecimal',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT'},

        'ui:outputDate' : {
                    'class':'String',
                    'format':'String',
                    'langLocale':'String',
                    'value':'String',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT'},

        'ui:outputDateTime' : {
                    'class':'String',
                    'format':'String',
                    'langLocale':'String',
                    'timezone':'String',
                    'value':'String',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT'},

        'ui:outputEmail' : {
                    'class':'String',
                    'value':'String',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT'},

        'ui:outputNumber' : {
                    'class':'String',
                    'format':'String',
                    'value':'BigDecimal',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT'},

        'ui:outputPhone' : {
                    'class':'String',
                    'value':'String',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT'},

        'ui:outputRichText' : {
                    'class':'String',
                    'linkify':'Boolean',
                    'value':'String',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT'},

        'ui:outputText' : {
                    'class':'String',
                    'title':'String',
                    'value':'String',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT'},

        'ui:outputTextArea' : {
                    'class':'String',
                    'linkify':'Boolean',
                    'value':'String',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT'},

        'ui:outputURL' : {
                    'alt':'String',
                    'class':'String',
                    'disabled':'Boolean',
                    'iconClass':'String',
                    'label':'String',
                    'target':'String',
                    'title':'String',
                    'value':'String',
                    'dblclick':'COMPONENT',
                    'mouseover':'COMPONENT',
                    'mouseout':'COMPONENT',
                    'mouseup':'COMPONENT',
                    'mousemove':'COMPONENT',
                    'mousedown':'COMPONENT',
                    'click':'COMPONENT'},

        'ui:scrollerWrapper' : {'class':'String'},

        'ui:spinner' : {
                    'class':'String',
                    'isVisible':'Boolean',
                    'toggle':'COMPONENT'}


    }


    return tag_dict


class AuraTagCompletions(sublime_plugin.EventListener):
    """
    Provide tag completions for HTML
    It matches just after typing the first letter of a tag name
    """
    def __init__(self):  
        completion_list = self.default_completion_list()
        self.prefix_completion_dict = {}
        # construct a dictionary where the key is first character of
        # the completion list to the completion
        for s in completion_list:
            prefix = s[0][0]
            self.prefix_completion_dict.setdefault(prefix, []).append(s)

        # construct a dictionary from (tag, attribute[0]) -> [attribute]
        self.tag_to_attributes = get_tag_to_attributes()

    def on_query_completions(self, view, prefix, locations):
        # Only trigger within HTML
        
        # if view.match_selector(locations[0], "text.html meta.tag meta.attribute-with-value.html string.quoted.double.html punctuation.definition.string.end.html"):
        #     self.expand_tag_attributes(view, locations)
        #     return ([('public', 'public'),('private\tString', 'private'), ('global','global')], sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)

        print("prefix:", prefix)
        if not view.match_selector(locations[0], "text.html - source - string.quoted"):
            return []

        # check if we are inside a tag
        is_inside_tag = view.match_selector(locations[0],
                "text.html meta.tag - text.html punctuation.definition.tag.begin")

        return self.get_completions(view, prefix, locations, is_inside_tag)

    def get_completions(self, view, prefix, locations, is_inside_tag):
        # see if it is in tag.attr or tag#attr format
        pt = locations[0] - len(prefix) - 1
        ch = view.substr(sublime.Region(pt, pt + 1))

        if ch == ':':
            prefix = self.expand_tag_attributes(view, locations)
            ch = '<'


        print('prefix:', prefix)
        print("ch", ch)
        print('is_inside_tag', is_inside_tag)

        completion_list = []
        if is_inside_tag and ch != '<':
            if ch in [' ', '\t', '\n']:
                # maybe trying to type an attribute
                completion_list = self.get_attribute_completions(view, locations[0], prefix)
            # only ever trigger completion inside a tag if the previous character is a <
            # this is needed to stop completion from happening when typing attributes
            return (completion_list, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)

        if prefix == '':
            # need completion list to match
            return ([], sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)

        # match completion list using prefix
        completion_list = self.prefix_completion_dict.get(prefix[0], [])
        # if the opening < is not here insert that
        if ch != '<':
            completion_list = [(pair[0], '<' + pair[1]) for pair in completion_list]

        flags = 0
        if is_inside_tag:
            flags = sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS

        return (completion_list, flags)

    def default_completion_list(self):
        """
        Generate a default completion list for HTML
        """

        # print('default_completion_list')
        default_list = []
        normal_tags = ([
            'aura:attribute',
            'aura:if',
            'aura:iteration',
            'aura:set',
            'aura:registerEvent',
            'aura:event',
            'aura:handler',
            'aura:component',
            'aura:dependency',
            'aura:interface',
            'aura:method',
            'aura:expression',
            'aura:html',
            'aura:renderif',
            'aura:unescapedHtml',
            'auraStorage:init',
            'force:canvasApp',
            'force:inputField',
            'force:outputField',
            'force:recordEdit',
            'force:recordView',
            'forceChatter:feed',
            'forceChatter:fullFeed',
            'forceChatter:publisher',
            'lightning:badge',
            'lightning:button',
            'lightning:buttonGroup',
            'lightning:buttonIcon',
            'lightning:buttonMenu',
            'lightning:card',
            'lightning:formattedDateTime',
            'lightning:formattedNumber',
            'lightning:icon',
            'lightning:Input',
            'lightning:layout',
            'lightning:layoutItem',
            'lightning:menuItem',
            'lightning:select',
            'lightning:spinner',
            'lightning:tab',
            'lightning:tabset',
            'lightning:textarea',
            'ltng:require',
            'ui:actionMenuItem',
            'ui:button',
            'ui:checkboxMenuItem',
            'ui:inputCheckbox',
            'ui:inputCurrency',
            'ui:inputDate',
            'ui:inputDateTime',
            'ui:inputDefaultError',
            'ui:inputEmail',
            'ui:inputNumber',
            'ui:inputPhone',
            'ui:inputRadio',
            'ui:inputRichText',
            'ui:inputSecret',
            'ui:inputSelect',
            'ui:inputSelectOption',
            'ui:inputText',
            'ui:inputTextArea',
            'ui:inputURL',
            'ui:menu',
            'ui:menuItem',
            'ui:menuItemSeparator',
            'ui:menuList',
            'ui:menuTrigger',
            'ui:menuTriggerLink',
            'ui:message',
            'ui:outputCheckbox',
            'ui:outputCurrency',
            'ui:outputDate',
            'ui:outputDateTime',
            'ui:outputEmail',
            'ui:outputNumber',
            'ui:outputPhone',
            'ui:outputRichText',
            'ui:outputText',
            'ui:outputTextArea',
            'ui:outputURL',
            'ui:scrollerWrapper',
            'ui:spinner'
        ])

        for tag in normal_tags:
            default_list.append(make_completion(tag))
            default_list.append(make_completion(tag.upper()))

        return default_list

    # This responds to on_query_completions, but conceptually it's expanding
    # expressions, rather than completing words.
    #
    # It expands these simple expressions:
    # tag.class
    # tag#id
    def expand_tag_attributes(self, view, locations):
        # Get the contents of each line, from the beginning of the line to
        # each point
        lines = [view.substr(sublime.Region(view.line(l).a, l))
            for l in locations]

        # print("lines:", lines)
        # Reverse the contents of each line, to simulate having the regex
        # match backwards
        lines = [l[::-1] for l in lines]

        # Check the first location looks like an expression
        # print('line:', lines[0])
        rex = re.compile("([\w:]+)")
        expr = match(rex, lines[0])

        # print("match:", rex.match(lines[0]) )
        # print("search:", rex.findall(lines[0]) )


        if not expr:
            # print("not expr")
            return []

        # Ensure that all other lines have identical expressions
        for i in range(1, len(lines)):
            ex = match(rex, lines[i])
            if ex != expr:
                return []

        # Return the completions
        tag = rex.match(expr).groups()[0][::-1]
        # print("tag2:", tag)

        return tag

    def get_attribute_completions(self, view, pt, prefix):
        SEARCH_LIMIT = 500
        search_start = max(0, pt - SEARCH_LIMIT - len(prefix))
        line = view.substr(sublime.Region(search_start, pt + SEARCH_LIMIT))

        line_head = line[0:pt - search_start]
        line_tail = line[pt - search_start:]

        # find the tag from end of line_head
        i = len(line_head) - 1
        tag = None
        space_index = len(line_head)
        while i >= 0:
            c = line_head[i]
            if c == '<':
                # found the open tag
                tag = line_head[i + 1:space_index]
                break
            elif c == ' ':
                space_index = i
            i -= 1

        # check that this tag looks valid
        # 
        if not tag:
            return []

        # determines whether we need to close the tag
        # default to closing the tag
        suffix = '>'

        for c in line_tail:
            if c == '>':
                # found end tag
                suffix = ''
                break
            elif c == '<':
                # found another open tag, need to close this one
                break

        if suffix == '' and not line_tail.startswith(' ') and not line_tail.startswith('>'):
            # add a space if not there
            suffix = ' '

        # got the tag, now find all attributes that match
        attributes = self.tag_to_attributes.get(tag, [])
        # ("class\tAttr", "class="$1">"),
        attri_completions = [ (name + '\t' + type, name + '="${0:'+ type +'}"' + suffix) for name,type in attributes.items()]
        return attri_completions


# unit testing
# to run it in sublime text:
# import HTML.html_completions
# HTML.html_completions.Unittest.run()

import unittest

class Unittest(unittest.TestCase):

    class Sublime:
        INHIBIT_WORD_COMPLETIONS = 1
        INHIBIT_EXPLICIT_COMPLETIONS = 2

    # this view contains a hard coded one line super simple HTML fragment
    class View:
        def __init__(self):
            self.buf = '<tr><td class="a">td.class</td></tr>'

        def line(self, pt):
            # only ever 1 line
            return sublime.Region(0, len(self.buf))

        def substr(self, region):
            return self.buf[region.a : region.b]

    def run():
        # redefine the modules to use the mock version
        global sublime

        sublime_module = sublime
        # use the normal region
        Unittest.Sublime.Region = sublime.Region
        sublime = Unittest.Sublime

        test = Unittest()
        test.test_simple_completion()
        test.test_inside_tag_completion()
        test.test_inside_tag_no_completion()
        test.test_expand_tag_attributes()

        # set it back after testing
        sublime = sublime_module

    # def get_completions(self, view, prefix, locations, is_inside_tag):
    def test_simple_completion(self):
        # <tr><td class="a">td.class</td></tr>
        view = Unittest.View()
        completor = HtmlTagCompletions()

        # simulate typing 'tab' at the start of the line, it is outside a tag
        completion_list, flags = completor.get_completions(view, 'tab', [0], False)

        # should give a bunch of tags that starts with t
        self.assertEqual(completion_list[0], ('table\tTag', '<table>$0</table>'))
        self.assertEqual(completion_list[1], ('tbody\tTag', '<tbody>$0</tbody>'))
        # don't suppress word based completion
        self.assertEqual(flags, 0)

    def test_inside_tag_completion(self):
        # <tr><td class="a">td.class</td></tr>
        view = Unittest.View()
        completor = HtmlTagCompletions()

        # simulate typing 'h' after <tr><, i.e. <tr><h
        completion_list, flags = completor.get_completions(view, 'h', [6], True)

        # should give a bunch of tags that starts with h, and without <
        self.assertEqual(completion_list[0], ('head\tTag', 'head>$0</head>'))
        self.assertEqual(completion_list[1], ('header\tTag', 'header>$0</header>'))
        self.assertEqual(completion_list[2], ('h1\tTag', 'h1>$0</h1>'))
        # suppress word based completion
        self.assertEqual(flags, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)

        # simulate typing 'he' after <tr><, i.e. <tr><he
        completion_list, flags = completor.get_completions(view, 'he', [7], True)

        # should give a bunch of tags that starts with h, and without < (it filters only on the first letter of the prefix)
        self.assertEqual(completion_list[0], ('head\tTag', 'head>$0</head>'))
        self.assertEqual(completion_list[1], ('header\tTag', 'header>$0</header>'))
        self.assertEqual(completion_list[2], ('h1\tTag', 'h1>$0</h1>'))
        # suppress word based completion
        self.assertEqual(flags, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)

    def test_inside_tag_no_completion(self):
        # <tr><td class="a">td.class</td></tr>
        view = Unittest.View()
        completor = HtmlTagCompletions()

        # simulate typing 'h' after <tr><td , i.e. <tr><td h
        completion_list, flags = completor.get_completions(view, 'h', [8], True)

        # should give nothing, but disable word based completions, since it is inside a tag
        self.assertEqual(completion_list, [])
        self.assertEqual(flags, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)

    def test_expand_tag_attributes(self):
        # <tr><td class="a">td.class</td></tr>
        view = Unittest.View()
        completor = HtmlTagCompletions()

        # simulate typing tab after td.class
        completion_list, flags = completor.get_completions(view, '', [26], False)

        # should give just one completion, and suppress word based completion
        self.assertEqual(completion_list, [('td.class', '<td class="class">$1</td>$0')])
        self.assertEqual(flags, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)
